#common routines for dealing with rom images and romantic comedies
from inc_noesis import *
import os


ReadRomImageFlag_None = 0
ReadRomImageFlag_Interleave = (1 << 0)
ReadRomImageFlag_EndianSwap_Word = (1 << 1)
ReadRomImageFlag_EndianSwap_DWord = (1 << 2)

def readRomImages(imageBasePath, imageSet, imageSize, flags = ReadRomImageFlag_None, printStatus = False, interleaveSize = 1):
	imageCount = len(imageSet)
	data = bytearray()
	for imageIndex in range(0, imageCount):
		imagePath = imageSet[imageIndex]
		imageFilePath = os.path.join(imageBasePath, imagePath)
		imageFileSize = os.path.getsize(imageFilePath)
		if imageFileSize != imageSize:
			if printStatus:
				print("Bad/no image -", imageFileSize, "-", imageFilePath)
			return None
		if printStatus:
			print("Loading", imageFilePath)
		with open(imageFilePath, "rb") as f:
			data += f.read()
			
	if flags & ReadRomImageFlag_Interleave:
		data = noesis.interleaveUniformBytes(data, interleaveSize, imageSize // interleaveSize)
	if flags & ReadRomImageFlag_EndianSwap_Word:
		data = noesis.swapEndianArray(data, 2)
	if flags & ReadRomImageFlag_EndianSwap_DWord:
		data = noesis.swapEndianArray(data, 4)
		
	return data


#well, just in case we don't feel like hardcoding or defining tile dimensions over and over again
NesTileWidth = NesTileHeight = 8
SnesTileWidth = SnesTileHeight = 8
VdpTileWidth = VdpTileHeight = 8


def nesGetChrOffsetAndSize(data):
	chrOffset = -1
	chrSize = -1
	if len(data) >= 16:
		tag, prgSize, chrSize, f6 = noeUnpack("<IBBB", data[:7])
		if tag == 0x1A53454E:
			chrOffset = 16 + (prgSize << 14)
			if f6 & 2:
				chrOffset += 512
			chrSize <<= 13
	return chrOffset, chrSize


#snes address to file functions assume a headerless image

def snesHiRomPtrToFileOffset(addr):
	if addr == 0:
		return 0
	if addr >= 0xC00000:
		return addr - 0xC00000
	#assume we're using the other set of linear banks
	return addr - 0x400000

def snesLoRomPtrToFileOffset(addr):
	if addr == 0:
		return 0
	if addr >= 0x800000:
		addr -= 0x800000
	bank = (addr >> 16)
	if not bank & 1:
		addr -= 0x8000
	bank >>= 1
	return (bank << 16) | (addr & 0xFFFF)

def snesFileOffsetToLoRomPtr(offset, bankRebase = 0x80):
	if offset == 0:
		return 0
	bank = offset >> 16
	addr = offset & 0xFFFF
	bank <<= 1
	if addr >= 0x8000:
		bank += 1
		addr -= 0x8000

	bank += bankRebase
	addr += 0x8000
	
	return (bank << 16) | addr
	
def snesGetGameTitleExplicit(data, isLoRom):
	titleStart = 0x7FC0 if isLoRom else 0xFFC0
	if (titleStart + 21) > len(data):
		return ""
	try:
		title = noeStrFromBytes(data[titleStart : titleStart + 21]).rstrip(" ")
		return title
	except:
		return ""
		
def snesGetGameTitle(data):
	try:
		data = snesSkipReaderHeader(data)
		return snesGetGameTitleExplicit(data, snesIsLoRom(data))
	except:
		return ""
	
def snesSkipReaderHeader(data):
	smcSize = len(data) & 1023
	if smcSize:
		data = data[smcSize:]
	return data
	
def snesIsLoRom(data):
	nchecskum, checskum = noeUnpack("<HH", data[0x7FDC:0x7FE0])
	return (checskum ^ nchecskum) == 0xFFFF

def snesGetHeaderOffset(isLoRom):
	return 0x7FC0 if isLoRom else 0xFFC0
	
def snesGetChecksum(data, isLoRom):
	chkOffset = snesGetHeaderOffset(isLoRom) + 0x1C + 2
	return noeUnpack("<H", data[chkOffset : chkOffset + 2])[0]

def snesCalcChecksum(data, isLoRom):
	#haven't tested this over a very wide variety of data, it's possible that more exceptions exist
	dataSize = len(data)
	dupSizeLut = (0x80000, 0x100000, 0x200000, 0x200000, 0x400000)
	dupChunkSize = dupSizeLut[min(dataSize >> 20, len(dupSizeLut) - 1)]
	dupSize = dataSize & (dupChunkSize - 1)
	cdata = bytearray(data) + data[dataSize - dupSize:] * ((dupChunkSize // dupSize) - 1) if dupSize > 0 else data
	chkOffset = snesGetHeaderOffset(isLoRom) + 0x1C
	cdata[chkOffset + 0] = cdata[chkOffset + 1] = 0xFF
	cdata[chkOffset + 2] = cdata[chkOffset + 3] = 0x00
	checksum = 0
	for offset in range(len(cdata)):
		checksum = (checksum + cdata[offset]) & 0xFFFF
	return checksum

def snesRecalcChecksum(data, isLoRom):
	checksum = snesCalcChecksum(data, isLoRom)
	nchecksum = checksum ^ 0xFFFF
	chkOffset = snesGetHeaderOffset(isLoRom) + 0x1C
	data[chkOffset : chkOffset + 4] = noePack("<HH", nchecksum, checksum)


def gameboyGetChecksum(data):
	headerChecksum, checksum = noeUnpack(">BH", data[0x14D : 0x150])
	return checksum | (headerChecksum << 16)

def gameboyCalcChecksum(data):
	headerChecksum = 0
	for offset in range(0x134, 0x14D):
		headerChecksum = (headerChecksum - data[offset] - 1) & 0xFF

	checksum = 0
	for offset in range(0x14E):
		checksum = (checksum + data[offset]) & 0xFFFF
	for offset in range(0x150, len(data)):
		checksum = (checksum + data[offset]) & 0xFFFF
		
	return checksum | (headerChecksum << 16)
	
def gameboyRecalcChecksum(data):
	checksum = gameboyCalcChecksum(data)
	data[0x14D : 0x150] = noePack(">BH", (checksum >> 16) & 0xFF, checksum & 0xFFFF)


def genesisGetGameTitle(data, domestic = False, verifySega = True):
	offset = 0x120 if domestic else 0x150
	if offset + 48 > len(data):
		return ""
	try:
		if verifySega and data[0x100 : 0x104] != "SEGA".encode("ASCII"):
			return ""
		title = noeStrFromBytes(data[offset : offset + 48]).rstrip(" ")
		return title
	except:
		return ""	

def genesisGetChecksum(data):
	return noeUnpack(">H", data[0x18E : 0x190])[0]

def genesisCalcChecksum(data):
	checksum = 0
	for offset in range(0x200, len(data), 2):
		checksum = (checksum + (data[offset] << 8) + data[offset + 1]) & 0xFFFF
	return checksum

def genesisRecalcChecksum(data):
	checksum = genesisCalcChecksum(data)
	data[0x18E : 0x190] = noePack(">H", checksum)

VdpControlWordType_Invalid = -1
VdpControlWordType_Reg = 0
VdpControlWordType_Addr = 1
	
def genesisVdpGetCtrlType(cw):
	if (cw & 0xE000) == 0x8000:
		return VdpControlWordType_Reg
	elif (cw & 0xFF0C) == 0:
		return VdpControlWordType_Addr
	return VdpControlWordType_Invalid

def genesisVdpGetCtrlRegInfo(cw):
	regIndex = ((cw & 0x1F00) >> 8)
	data = (cw & 0xFF)
	return regIndex, data

def genesisVdpGetCtrlAddr(cw):
	return ((cw & 3) << 14) | ((cw & 0x3FFF0000) >> 16)
	
def genesisVdpGetCtrlAddrInfo(cw):
	memType = ((cw & 0x20) >> 4) | ((cw & 0x80000000) >> 31)
	isWrite = (cw & 0x40000000) != 0
	isDma = (cw & 0x80) != 0
	isVramSrc = (cw & 0x40) != 0
	return memType, isWrite, isDma, isVramSrc
