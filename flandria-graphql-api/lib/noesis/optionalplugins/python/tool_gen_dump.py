
#Dick's Data Dumper
#(c) 2021 Rich Whitehouse

from inc_noesis import *
import os
import time

"""
This script is meant to be used with the following components:

	tool_gen_dump_USERMAIN.BIN
	Genesis MAIN-CPU binary. You can build this into an image using the tool_gen_makecd script. Replace tool_gen_makecd_USERMAIN.BIN with this file and you can build the image with the rest of the data as-is.
	Remember to adjust MIN_IMAGE_SIZE and MIN_AUDIO_SIZE in the tool_gen_makecd script if necessary to produce an image usable with your CD burner. I'd set both to 0x2000000 or so to be safe.

	tool_gen_dump_ARDUINO.ino
	Arduino sketch, only tested on an Arduino Uno.
	By default, you'll need to wire pins 1..9 (excluding +5V and GND) from player 2's controller port to pins 2..8 on the Arduino. There's an array near the top of the sketch to change this mapping if necessary.
	This can be accomplished pretty easily using a standard Genesis controller extension cable and some wires, with an optional DE-9 terminal block.

With the binary running on your Sega Genesis (and/or Sega CD), run the sketch on your Arduino as well, then you can use the poke/dump tool options in Noesis from this script to communicate with the Arduino.
Note that you'll probably want to change GENESIS_DUMP_ADDRESS to 0x00400000 if you're looking to dump a cart via Sega CD using the "disconnect (or put some tape over) B32" trick. If you need to deal with
special mapping hardware, you can write to registers using the SERIAL_CMD_POKE_DATA command in between dumps as well. You can do this rather tediously through the Noesis menu, but you'd probably be better off
adding a few lines of script here to automate it depending on your needs.

The Genesis-Arduino protocol packs checksum bits into the pins along with the data on the Genesis side and verifies them on the Arduino side. The Arduino then calculates its own 32-bit checksum which is sent
over COM and verified in this script for each data packet. These are simple checksum algorithms and are not failsafe, but there's still a pretty good chance that they'll save you from producing a bad dump.
"""

SERIAL_READ_TIMEOUT = 2.0 #in seconds
SERIAL_BAUD = 115200 #should match skSerialBaudRate on the arduino side
TARGET_ENDIAN = "<"

GENESIS_DUMP_ADDRESS = 0x00000000 #must be dword-aligned (note that if you're dumping from the sega cd, cart rom is mapped to 0x00400000)
GENESIS_DUMP_SIZE = 0x00200000
#to verify ram pokes
#GENESIS_DUMP_ADDRESS = 0x00FF2000
#GENESIS_DUMP_SIZE = 0x00000100

#as an example, this is a ram address, but the idea is that this can also be used to poke registers and control cart mapping if necessary.
GENESIS_POKE_ADDRESS = 0x00FF2000
GENESIS_POKE_VALUE = 0x12345678
GENESIS_POKE_TYPE = 2 #2=dword, 1=word, 0=byte

SERIAL_CMD_READ_DATA = 1
SERIAL_CMD_POKE_DATA = 2


def registerNoesisTypes():
	handle = noesis.registerTool("Dump via COM", lambda toolIndex: genericComOp(dumpOp), "Trigger a dump through an Arduino serial connection.")
	noesis.setToolSubMenuName(handle, "Genesis")
	
	handle = noesis.registerTool("Poke via COM", lambda toolIndex: genericComOp(pokeOp), "Poke memory through an Arduino serial connection.")
	noesis.setToolSubMenuName(handle, "Genesis")
	
	return 1


def dumpOp(portHandle):
	if noesis.comWrite(portHandle, createCommand(SERIAL_CMD_READ_DATA, GENESIS_DUMP_ADDRESS, GENESIS_DUMP_SIZE)) < 16:
		print("Failed to send dump command over COM.")
	else:
		dumpedData = bytearray()
		lastReadTime = time.time()
		currentBuffer = bytearray()
		while True:
			data = noesis.comRead(portHandle, 0x80 + 12)
			currentTime = time.time()
			if len(data) > 0:
				currentBuffer += data
				lastReadTime = currentTime
			if len(currentBuffer) >= 4:
				msgId = noeUnpack(TARGET_ENDIAN + "I", currentBuffer[:4])[0]
				if msgId == 0x3A47534D:
					endLine = currentBuffer.find(b"\n")
					if endLine >= 0: #if we don't have an endline yet, continue reading until we get one (or we time out)
						msg = currentBuffer[:endLine].decode("ASCII")
						print(msg.replace("\r", ""))
						currentBuffer = currentBuffer[endLine + 1:]
				elif msgId == 0x1337D474:
					if len(currentBuffer) >= 12:
						dataChk, dataSize = noeUnpack(TARGET_ENDIAN + "II", currentBuffer[4:12])
						totalSize = 12 + dataSize
						if len(currentBuffer) >= totalSize:
							dataChunk = currentBuffer[12:totalSize]
							verifyChk = sum(noeUnpack(TARGET_ENDIAN + "%iI"%(len(dataChunk) // 4), dataChunk)) & 0xFFFFFFFF
							if dataChk != verifyChk:
								print("Aborting, bad checksum on data chunk. %08X vs %08X"%(dataChk, verifyChk))
								break
							dumpedData += dataChunk
							if len(dumpedData) >= GENESIS_DUMP_SIZE:
								break
							currentBuffer = currentBuffer[totalSize:]
							noesis.pumpModalStatus("Transferred %i / %i bytes."%(len(dumpedData), GENESIS_DUMP_SIZE), 3.0)
				else:
					print("Unrecognized message from target: %08X"%msgId, "-", currentBuffer)
					break
			
			if (currentTime - lastReadTime) > SERIAL_READ_TIMEOUT:
				print("Transfer timed out.")
				break
	
	noesis.clearModalStatus()
	
	if len(dumpedData) > 0:
		savePath = noesis.userPrompt(noesis.NOEUSERVAL_SAVEFILEPATH, "Save Data", "Select destination for the dumped data.", os.path.join(noesis.getSelectedDirectory(), "GENESIS_DUMP.BIN"), None)
		if savePath:
			with open(savePath, "wb") as fw:
				fw.write(dumpedData)

				
def pokeOp(portHandle):
	if noesis.comWrite(portHandle, createCommand(SERIAL_CMD_POKE_DATA, GENESIS_POKE_ADDRESS, GENESIS_POKE_VALUE, GENESIS_POKE_TYPE)) < 16:
		print("Failed to send poke command over COM.")
	try:
		print("Poke response:", noesis.comRead(portHandle, 2048).decode("ASCII"))
	except:
		pass


def genericComOp(comOp):
	noesis.logPopup()

	comPorts = noesis.comGetPortPaths()
	if len(comPorts) == 0:
		print("No COM ports were detected.")
		return 0
		
	portDict = {}
	for portIndex, portPath in comPorts:
		print("COM%i -"%portIndex, portPath)
		portDict[portIndex] = portPath

	selectedPortIndex = noesis.userPrompt(noesis.NOEUSERVAL_INT, "COM Port", "Enter the number of the desired COM port.", str(comPorts[0][0]), None)
	if selectedPortIndex is None:
		return 0

	portHandle = noesis.comOpenPort(selectedPortIndex)
	if portHandle < 0:
		print("Failed to open COM handle.")
		return 0

	timeouts = noesis.comGetTimeouts(portHandle)
	noesis.comSetTimeouts(portHandle, 1, 1, 1, 1, 1)
		
	baudRate, byteSize, parity, stopBits = noesis.comGetInfo(portHandle)
	if baudRate != SERIAL_BAUD or byteSize != 8 or parity != 0 or stopBits != 1:
		print("Setting desired baud rate:", SERIAL_BAUD)
		noesis.comSetInfo(portHandle, SERIAL_BAUD, 8, 0, 1)
		
	#empty out any tiny bits of data that might be in the read buffer before we start writing
	for i in range(128):
		if len(noesis.comRead(portHandle, 128)) == 0:
			break
		time.sleep(0.1)
	
	comOp(portHandle)
	
	noesis.comClosePort(portHandle)
	
	return 0

def createCommand(cmd, p0 = 0, p1 = 0, p2 = 0):
	return noePack(TARGET_ENDIAN + "IIII", cmd, p0, p1, p2)
