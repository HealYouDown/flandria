
//Dick's Data Dumper
//(c) 2021 Rich Whitehouse

static const int32_t skPinCount = 7;

//times are in ms
static const uint32_t skMaxTransferWaitTimeout = 500;
static const int skIdleDelay = 100;
static const int skResetDelay = 100;

//feel free to go higher, but it may trigger checksum errors.
//if you're having problems, 9600 should be safest across the board.
//should match SERIAL_BAUD on the noesis side.
static const uint32_t skSerialBaudRate = 115200;
static const uint32_t skSerialConfig = SERIAL_8N1;

//this maps us from genesis pin (D0..TH) to arduino pin.
static const uint8_t skPinMap[skPinCount] =
{
  2, 3, 4, 5, 6, 7, 8
};

#define GEN_D0  0
#define GEN_D1  1
#define GEN_D2  2
#define GEN_D3  3
#define GEN_TL  4
#define GEN_TR  5
#define GEN_TH  6

#define SERIAL_CMD_READ_DATA  1
#define SERIAL_CMD_POKE_DATA  2

struct SSerialParams
{
  uint32_t mCmd;
  uint32_t mData[3];
};

static const uint8_t skPinWriteMask_Out = 0x3F;
static const uint8_t skPinWriteMask_In = 0x20;
static const uint8_t skPinReadMask_Out = 0x40;
static const uint8_t skPinReadMask_In = 0x5F;

//making the buffer too large might cause a transfer timeout, depending on your arduino and baud rate.
static const uint32_t skSerialOutBufferSize = 0x80;
static uint8_t sSerialOutBuffer[skSerialOutBufferSize];
static uint32_t sSerialChecksum = 0;
static uint32_t sSerialOutOffset = 0;

static int32_t sPinState = -1;

static void write_serial_msg(const char *pMsg, ...)
{
  char finalString[256];
  va_list args;
  va_start(args, pMsg);
  vsnprintf(finalString, 256, pMsg, args);
  va_end(args);

  Serial.print("MSG:");
  Serial.print(finalString);
  Serial.println();
}

static uint8_t get_pin_bits(const uint8_t readMask)
{
  uint8_t v = 0;
  for (int i = 0; i < skPinCount; ++i)
  {
    const uint8_t pinBit = (1 << i);
    if ((readMask & pinBit) && digitalRead(skPinMap[i]))
    {
      v |= pinBit;
    }
  }
  return v;
}

static void set_pin_bits(const uint8_t writeMask, const uint8_t bits)
{
  //order here is important, tr needs to be set after the other pins
  for (int i = 0; i < skPinCount; ++i)
  {
    const uint8_t pinBit = (1 << i);
    if (writeMask & pinBit)
    {
      digitalWrite(skPinMap[i], (bits & pinBit) ? HIGH : LOW);
    }
  }
  sPinState = bits;
}

static void set_pins_mode_out()
{
  for (int i = 0; i < skPinCount; ++i)
  {
    pinMode(skPinMap[i], OUTPUT);
  }
  pinMode(skPinMap[GEN_TH], INPUT);
}

static void set_pins_mode_in()
{
  for (int i = 0; i < skPinCount; ++i)
  {
    pinMode(skPinMap[i], INPUT);
  }
  pinMode(skPinMap[GEN_TR], OUTPUT);
}

void setup()
{
  Serial.begin(skSerialBaudRate, skSerialConfig);

  set_pins_mode_out();

  //set all pins high
  set_pin_bits(skPinWriteMask_Out, skPinWriteMask_Out);

  delay(skResetDelay);
}

template<bool wantHigh>
static bool wait_for_pin(const uint8_t pin)
{
  const uint8_t wantValue = (wantHigh) ? (1 << pin) : 0;
  const uint32_t startWaitTime = millis();
  while (true)
  {
    const int pinValue = digitalRead(skPinMap[pin]);
    if ((wantHigh && pinValue) || (!wantHigh && !pinValue))
    {
      return true;
    }

    const uint32_t currentTime = millis();
    if ((currentTime - startWaitTime) > skMaxTransferWaitTimeout)
    {
      break;
    }
  }
  return false;
}

template<int packCount>
static bool write_port_pack5bits(const uint64_t value)
{
  for (int i = 0; i < packCount; ++i)
  {
    const bool waitPin = (i & 1) ? wait_for_pin<true>(GEN_TH) : wait_for_pin<false>(GEN_TH);
    if (!waitPin)
    {
      return false;
    }
    const uint64_t bitOffset = (5 * packCount) - i * 5 - 5;
    const uint8_t trBit = (i & 1) ? (1 << GEN_TR) : 0;
    set_pin_bits(skPinWriteMask_Out, ((value >> bitOffset) & 0x1F) | trBit);
  }
  return true;
}

static bool write_port_30(const uint32_t value)
{
  return write_port_pack5bits<6>(value);
}

static bool write_port_40(const uint32_t value0, const uint8_t value1)
{
  const uint32_t secondPack = (value0 & 3) | ((uint32_t)value1 << 2);
  return write_port_pack5bits<6>(value0 >> 2) && write_port_pack5bits<2>(secondPack);
}

static void flush_serial_buffer()
{
  if (sSerialOutOffset > 0)
  {
    uint32_t outHeader[3];
    outHeader[0] = 0x1337D474;
    outHeader[1] = sSerialChecksum;
    outHeader[2] = sSerialOutOffset;
    Serial.write((char *)outHeader, sizeof(outHeader));
    Serial.write((char *)sSerialOutBuffer, sSerialOutOffset);
    sSerialChecksum = 0;
    sSerialOutOffset = 0;
  }
}

static void buffered_dword_out(const uint8_t *pData)
{
  //swap endian while we're at it, since we're reading data as dwords on the genesis side
  sSerialOutBuffer[sSerialOutOffset + 0] = pData[3];
  sSerialOutBuffer[sSerialOutOffset + 1] = pData[2];
  sSerialOutBuffer[sSerialOutOffset + 2] = pData[1];
  sSerialOutBuffer[sSerialOutOffset + 3] = pData[0];
  sSerialChecksum += *(uint32_t *)(&sSerialOutBuffer[sSerialOutOffset]);
  sSerialOutOffset += 4;
  if (sSerialOutOffset >= skSerialOutBufferSize)
  {
    flush_serial_buffer(); 
  }
}

static bool unpack_dwords(const uint32_t currentOffset, const uint8_t *pData)
{
  const uint8_t tlBit = (1 << GEN_TL);
  const uint32_t dataMask = 0x0F;

  const uint32_t dw0 = ((uint32_t)pData[0] & dataMask) |
                       (((uint32_t)pData[1] & dataMask) << 4UL) |
                       (((uint32_t)pData[2] & dataMask) << 8UL) |
                       (((uint32_t)pData[3] & dataMask) << 12UL) |
                       (((uint32_t)pData[4] & dataMask) << 16UL) |
                       (((uint32_t)pData[5] & dataMask) << 20UL) |
                       (((uint32_t)pData[6] & dataMask) << 24UL) |
                       (((uint32_t)pData[7] & dataMask) << 28UL);
  const uint32_t dw1 = ((uint32_t)pData[8] & dataMask) |
                       (((uint32_t)pData[9] & dataMask) << 4UL) |
                       (((uint32_t)pData[10] & dataMask) << 8UL) |
                       (((uint32_t)pData[11] & dataMask) << 12UL) |
                       (((uint32_t)pData[12] & dataMask) << 16UL) |
                       (((uint32_t)pData[13] & dataMask) << 20UL) |
                       (((uint32_t)pData[14] & dataMask) << 24UL) |
                       (((uint32_t)pData[15] & dataMask) << 28UL);
  const uint16_t chk = ((pData[0] & tlBit) >> 4) | ((pData[1] & tlBit) >> 3) |
                       ((pData[2] & tlBit) >> 2) | ((pData[3] & tlBit) >> 1) |
                       ((pData[4] & tlBit) >> 0) | ((pData[5] & tlBit) << 1) |
                       ((pData[6] & tlBit) << 2) | ((pData[7] & tlBit) << 3) |
                       ((pData[8] & tlBit) << 4) | ((pData[9] & tlBit) << 5) |
                       ((pData[10] & tlBit) << 6) | ((pData[11] & tlBit) << 7) |
                       ((pData[12] & tlBit) << 8) | ((pData[13] & tlBit) << 9) |
                       ((pData[14] & tlBit) << 10) | ((pData[15] & tlBit) << 11);
  const uint32_t chk0 = dw0 + dw1;
  uint16_t chk1 = (chk0 & 0xFFFF);
  chk1 += (chk0 >> 16UL);
  if (chk1 != chk)
  {
    write_serial_msg("Bad checksum at %08lX - %04lX vs %04lX", currentOffset, chk, chk1);
    return false;
  }
  buffered_dword_out((const uint8_t *)&dw0);
  buffered_dword_out((const uint8_t *)&dw1);
  return true;
}

static bool data_transfer(const uint32_t expectedSize)
{
  sSerialOutOffset = 0;
  sSerialChecksum = 0;
  
  uint32_t dw;
  uint32_t chk;
  uint8_t readBuffer[16];
  set_pin_bits(skPinWriteMask_In, 0);

  uint32_t receivedSize = 0;
  while (receivedSize < expectedSize)
  {
    for (int i = 0; i < 16; i += 2)
    {
      wait_for_pin<false>(GEN_TH);
      readBuffer[i + 0] = get_pin_bits(skPinReadMask_In);
      set_pin_bits(skPinWriteMask_In, skPinWriteMask_In);
      wait_for_pin<true>(GEN_TH);
      readBuffer[i + 1] = get_pin_bits(skPinReadMask_In);
      set_pin_bits(skPinWriteMask_In, 0);
    }
    if (!unpack_dwords(receivedSize, readBuffer))
    {
      return false;
    }
    receivedSize += 8;
  }

  flush_serial_buffer();
  return true;
}

void loop()
{
  if (Serial.available() >= sizeof(SSerialParams))
  {
    SSerialParams params;
    Serial.readBytes((char *)&params, sizeof(params));
    write_serial_msg("Received command: %08lX / %08lX / %08lX / %08lX", params.mCmd, params.mData[0], params.mData[1], params.mData[2]);
    
    //tell the other side we're ready to begin a transfer
    const int32_t desiredPinState = 0x2A;
    if (sPinState != desiredPinState)
    {
      set_pin_bits(skPinWriteMask_Out, desiredPinState);
    }
    switch (params.mCmd)
    {
    case SERIAL_CMD_READ_DATA:
      if (write_port_30(0x1337F4C3))
      {
        write_port_30(params.mData[0] >> 2);
        write_port_30(params.mData[1]);

        set_pins_mode_in();
        if (data_transfer(params.mData[1]))
        {
          write_serial_msg("Transfer complete.");
        }
      }
      else
      {
        write_serial_msg("Failed to write 30-bit command.");
      }
      break;
    case SERIAL_CMD_POKE_DATA:
      {
        const uint32_t pokeType = params.mData[2];
        if (pokeType < 3)
        {
          const uint32_t pokeCmdMap[3] = { 0x13370008, 0x13370016, 0x13370032 };
          if (write_port_30(pokeCmdMap[pokeType]))
          {
            switch (pokeType)
            {
            case 0:
              write_port_40(params.mData[0], (uint8_t)params.mData[1]);
              break;
            case 1:
              write_port_40(params.mData[0], 0);
              write_port_30(params.mData[1]);
              break;
            case 2:
              write_port_40(params.mData[0], 0);
              write_port_40(params.mData[1], 0);
              break;
            default:
              break;
            }
          }          
        }
      }
      break;
    default:
      write_serial_msg("Unknown command: %08lX", params.mCmd);
      break;
    }
    //reset after performing the command
    set_pins_mode_out();
    set_pin_bits(skPinWriteMask_Out, skPinWriteMask_Out);
    delay(skResetDelay);
  }
  else
  {
    delay(skIdleDelay);
  }
}
