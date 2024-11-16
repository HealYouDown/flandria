from inc_noesis import *
import os

#this script will construct a sega cd image using the following data:
EXPECTED_FILES = (
	"tool_gen_makecd_INITPRGU.BIN", #(U) main CPU initial program, typically <= 0x584 bytes at 0x200 bytes into sector 0, varies by region, must not exceed 0x600 bytes. you can snip this out of a retail image for other regions.
	"tool_gen_makecd_SCDMAIN.BIN", #main CPU initial program code to be run after standard INITPRGU code.
	"tool_gen_makecd_SCDSUB.BIN", #sub CPU initial program code.
	"tool_gen_makecd_USERMAIN.BIN", #your main CPU code. (you should provide this, but a default is provided with this script)
	"tool_gen_makecd_USERSUBC.BIN", #your sub CPU code. (you should provide this, but a default is provided with this script)
	"tool_gen_makecd_AUDIO00.BIN" #default audio track data.
)

#you can add anything else here that you want to access from the iso-9660 file system. (note that subdirectories aren't supported) file names longer than 8 will blindly use the last 8 characters.
#it's a pretty bad idea to actually use this file system at runtime, so if you're trying to make something performant, you should probably create your own binary blob and cook out offsets for your code to reference.
#then you can just use the file system one time to get the lba of the file, and use your cooked offsets/sizes to read portions of it as needed.
FS_DATA_FILES = (
	#the two user code binaries must be first in this list, as this defines directory order. for speed, the loader assumes that the first two files in the directory will be user code.
	"tool_gen_makecd_USERMAIN.BIN",
	"tool_gen_makecd_USERSUBC.BIN"
)

#add additional audio tracks here as desired. will be auto-padded to 2352 bytes.
AUDIO_FILES = (
	"tool_gen_makecd_AUDIO00.BIN",
)

DATE_YMD = (2021, 9, 30) #stick whatever date you'd like in here, or source it from the actual date
VOLUME_NAME = b"NOESISLOADR\0" #12 bytes
SYSTEM_NAME = b"NOESISLOADR\0" #12 bytes
VOLUME_DATE = ("%02i%02i%04i"%(DATE_YMD[1], DATE_YMD[2], DATE_YMD[0])).encode("ASCII") #just shoving a date in here like Sonic CD, this all falls under "system reservation area"
ROM_CONSOLENAME = b"SEGA GENESIS    " #16 bytes
ROM_COPYRIGHT = b"(C)T-DICK 2021  " #16 bytes
ROM_DOMESTICNAME = b"Noesis Loader                                   " #48 bytes
ROM_OVERSEASNAME = b"Noesis Loader                                   " #48 bytes
ROM_SERIALNUMBER = b"GM MK-0000 -00  " #16 bytes (overlaps checksum with spaces, this is what Sonic CD does)
ROM_IOSUPPORT = b"J               " #16 bytes
ROM_MODEMSUPPORT = b"            " #12 bytes
ROM_REGIONSUPPORT = b"JUE             " #16 bytes
ISO_VOL_NAME = b"Noesis Sega CD Image"

IP_DEFAULT_MAX_SIZE = 0x584
IP_MAX_SIZE = 0x600 - IP_DEFAULT_MAX_SIZE
SP_MAX_SIZE = 0x7000

MIN_IMAGE_SIZE = 0x10000 #in case the bios decides over-read
MIN_AUDIO_SIZE = 0 #you may need a minimum audio track size as well, if you have an especially pissy burner

ADD_PREGAP = True
#you'll want to set ADD_PREGAP to False and modify the non-pregap default if your audio data has gaps baked in
DEFAULT_AUDIO_GAP_CONFIG = "    INDEX 00 00:00:00\n    INDEX 01 00:02:00\n" if ADD_PREGAP else "    INDEX 00 00:00:00\n    INDEX 01 00:00:00\n"

OUTPUT_NAME_PREFIX = "SCD_IMAGE"


def registerNoesisTypes():
	handle = noesis.registerTool("Sega CD Builder", scdBuildToolMethod, "Build a Sega CD image.")
	noesis.setToolSubMenuName(handle, "Genesis")
	return 1


def scdBuildToolMethod(toolIndex):
	noesis.logPopup()
	selDir = noesis.getSelectedDirectory()
	expectedPaths = []
	expectedData = []
	for expectedFile in EXPECTED_FILES:
		fullPath = os.path.join(selDir, expectedFile)
		if not os.path.exists(fullPath):
			print("Missing expected file:", fullPath)
			return -1
		expectedPaths.append(fullPath)
		with open(fullPath, "rb") as f:
			expectedData.append(f.read())
	
	ipDefaultData, mainData, subData, _, _, _ = expectedData
	if len(ipDefaultData) > IP_DEFAULT_MAX_SIZE:
		print("Initial program is too large:", len(ipDefaultData))
		return -1
	if len(mainData) > IP_MAX_SIZE:
		print("Main program is too large:", len(mainData))
		return -1
	if len(subData) > SP_MAX_SIZE:
		print("Sub program is too large:", len(subData))
		return -1
	
	dBs = NoeBitStream(None, NOE_BIGENDIAN)
	dBs.writeBytes(b"SEGADISCSYSTEM  ")
	dBs.writeBytes(VOLUME_NAME)
	dBs.writeUShort(0x100) #volume version
	dBs.writeUShort(1) #medium type
	dBs.writeBytes(SYSTEM_NAME)
	dBs.writeUShort(0) #system version
	dBs.writeUShort(0) #reserved
	dBs.writeUInt(0x200) #ip load address
	dBs.writeUInt(IP_DEFAULT_MAX_SIZE + IP_MAX_SIZE) #ip size
	dBs.writeUInt(0) #ip start offset
	dBs.writeUInt(0) #ip required wram size
	dBs.writeUInt(0x1000) #sp load address
	dBs.writeUInt(SP_MAX_SIZE) #sp size
	dBs.writeUInt(0) #sp start offset
	dBs.writeUInt(0) #sp required wram size
	dBs.writeBytes(VOLUME_DATE.ljust(176, b" "))

	dBs.writeBytes(ROM_CONSOLENAME)
	dBs.writeBytes(ROM_COPYRIGHT)
	dBs.writeBytes(ROM_DOMESTICNAME)
	dBs.writeBytes(ROM_OVERSEASNAME)
	dBs.writeBytes(ROM_SERIALNUMBER)
	dBs.writeBytes(ROM_IOSUPPORT)
	dBs.writeBytes(b" " * 28)
	dBs.writeBytes(ROM_MODEMSUPPORT)
	dBs.writeBytes(b" " * 40)
	dBs.writeBytes(ROM_REGIONSUPPORT)
	
	ipOffset = dBs.tell()
	if ipOffset != 0x200:
		print("Bad offset where IP should begin:", ipOffset)
		return -1
	
	#note that the bios has a copy of ipDefaultData and compares it before proceeding, so we can't change it (except to produce builds for different regions)
	dBs.writeBytes(ipDefaultData)
	dBs.padToSizeFromCurrentOffset(ipOffset + IP_DEFAULT_MAX_SIZE)
	dBs.writeBytes(mainData)
	
	#patch the sub header
	subData = bytearray(subData)
	subData[0x14 : 0x18] = noePack(">I", len(subData))
	
	dBs.padToSizeFromCurrentOffset(0x1000)
	dBs.writeBytes(subData)
	
	dBs.padToSizeFromCurrentOffset(0x8000)
	if not writeFileSystem(dBs, selDir):
		return -1
	
	t0Data = noePaddedByteArray(bytearray(dBs.getBuffer()), 0x800)
	
	track0LocalPath = OUTPUT_NAME_PREFIX + "_T00.BIN"
	
	cueData = "FILE \"" + track0LocalPath + "\" BINARY\n" + "  TRACK 01 MODE1/2048\n" + "    INDEX 01 00:00:00\n"

	track0Path = os.path.join(selDir, track0LocalPath)
	print("Writing", track0Path)
	with open(track0Path, "wb") as fw:
		fw.write(t0Data)

	for audioTrackIndex in range(len(AUDIO_FILES)):
		audioLocalPath = AUDIO_FILES[audioTrackIndex]
		audioInPath = os.path.join(selDir, audioLocalPath)
		audioOutLocalPath = OUTPUT_NAME_PREFIX + "_T%02i.BIN"%(1 + audioTrackIndex)
		
		cueData += "FILE \"" + audioOutLocalPath + "\" BINARY\n" + "  TRACK %02i AUDIO\n"%(2 + audioTrackIndex) + DEFAULT_AUDIO_GAP_CONFIG
		
		audioOutPath = os.path.join(selDir, audioOutLocalPath)
		print("Writing", audioOutPath)
		pregapData = bytearray()
		if ADD_PREGAP:
			pregapData += bytearray(2352 * 2 * 75)
		with open(audioInPath, "rb") as f, open(audioOutPath, "wb") as fw:
			audioData = pregapData + f.read()
			paddedSize = max(((len(audioData) + 2351) // 2352) * 2352, MIN_AUDIO_SIZE)
			fw.write(audioData.ljust(paddedSize, b"\0"))
			
	cueOutPath = os.path.join(selDir, OUTPUT_NAME_PREFIX + ".cue")
	print("Writing", cueOutPath)
	with open(cueOutPath, "w") as fw:
		fw.write(cueData)

	return 0

dualEndianDW = lambda v: noePack("<I", v) + noePack(">I", v)
dualEndianW = lambda v: noePack("<H", v) + noePack(">H", v)

def writeFileSystem(dBs, selDir):
	volumeStart = dBs.tell()
	vsLba = volumeStart >> 11
	leTableLba = vsLba + 2
	beTableLba = leTableLba + 1
	rootDirLba = beTableLba + 1

	#directory records
	rootRecords = NoeBitStream()
	fileData = bytearray()
	existingFiles = {}
	rootDotOffset = writeDirectoryRecord(rootRecords, ".", rootDirLba, 666)
	rootDotDotOffset = writeDirectoryRecord(rootRecords, "..", rootDirLba, 666)
	recordFixOffsets = []
	for localPath in FS_DATA_FILES:
		fileName, fileExt = os.path.splitext(localPath)
		if len(fileName) > 8:
			fileName = fileName[-8:]
		if len(fileExt) > 4:
			fileExt = fileExt[-4:]
			
		fsLocalPath = fileName + fileExt
			
		dupNameCount = existingFiles.get(fsLocalPath, 0)
		if dupNameCount:
			existingFiles[fsLocalPath] = dupNameCount + 1
			print("Duplicate filename after truncation:", fsLocalPath)
			if len(fileName) > 6:
				fileName = fileName[:6]
			fileName += "%02i"%dupNameCount
			fsLocalPath = fileName + fileExt
			print("New FS name will be:", fsLocalPath)
		else:
			existingFiles[fsLocalPath] = 1
		
		fullPath = os.path.join(selDir, localPath)
		if not os.path.exists(fullPath):
			print("Missing file:", fullPath)
			return False
		with open(fullPath, "rb") as f:
			data = f.read()
			paddedSize = (len(data) + 0x7FF) & ~0x7FF
			recordFixOffsets.append(writeDirectoryRecord(rootRecords, fsLocalPath.upper(), len(fileData) >> 11, len(data)))
			fileData += data.ljust(paddedSize, b"\0")
			
	rootRecordData = bytearray(rootRecords.getBuffer())
	rootRecordData = rootRecordData.ljust((len(rootRecordData) + 0x7FF) & ~0x7FF, b"\0")
	
	firstDataLba = rootDirLba + (len(rootRecordData) >> 11)
	#fix up root directory sizes
	rootRecordData[rootDotOffset + 10 : rootDotOffset + 18] = dualEndianDW(len(rootRecordData))
	rootRecordData[rootDotDotOffset + 10 : rootDotDotOffset + 18] = dualEndianDW(len(rootRecordData))
	#fix up data offsets
	for fixOffset in recordFixOffsets:
		currentLba = noeUnpack("<I", rootRecordData[fixOffset + 2 : fixOffset + 6])[0]
		rootRecordData[fixOffset + 2 : fixOffset + 10] = dualEndianDW(firstDataLba + currentLba)

	totalImageSize = max((firstDataLba << 11) + len(fileData), MIN_IMAGE_SIZE)
		
	#primary volume
	dBs.writeUByte(1) #type
	dBs.writeBytes(b"\x43\x44\x30\x30\x31") #id
	dBs.writeUByte(1) #version
	dBs.writeUByte(0)
	dBs.writeBytes(b"MEGA_CD".ljust(32, b" "))
	dBs.writeBytes(ISO_VOL_NAME.ljust(32, b" "))
	dBs.writeBytes(bytearray(8))
	dBs.writeBytes(dualEndianDW(totalImageSize >> 11)) #volume space
	dBs.writeBytes(bytearray(32))
	dBs.writeBytes(dualEndianW(1)) #set size
	dBs.writeBytes(dualEndianW(1)) #sequence number
	dBs.writeBytes(dualEndianW(0x800)) #logical block size
	dBs.writeBytes(dualEndianDW(0x0A)) #path table size (only supporting root, so only 1 entry)
	dBs.writeBytes(noePack("<II", leTableLba, 0) + noePack(">II", leTableLba, 0))
	writeDirectoryRecord(dBs, ".", rootDirLba, len(rootRecordData))
	dBs.writeBytes(b" " * 128)
	dBs.writeBytes(b"Noesis Sega CD Loader".ljust(128, b" "))
	dBs.writeBytes(b"Noesis Sega CD Loader".ljust(128, b" "))
	dBs.writeBytes(b"Noesis Sega CD Loader".ljust(128, b" "))
	dBs.writeBytes(b" " * 37)
	dBs.writeBytes(b" " * 37)
	dBs.writeBytes(b" " * 37)
	writeVolumeDate(dBs)
	writeVolumeDate(dBs)
	dBs.writeBytes(b"0" * 16 + b"\0")
	dBs.writeBytes(b"0" * 16 + b"\0")
	dBs.writeUByte(1)
	dBs.writeUByte(0)

	#volume terminator
	dBs.padToSizeFromCurrentOffset((vsLba + 1) << 11)
	dBs.writeUByte(0xFF)
	dBs.writeBytes(b"\x43\x44\x30\x30\x31")
	dBs.writeUByte(1)
	
	#path tables, pointing to nothing other than the root
	dBs.padToSizeFromCurrentOffset(leTableLba << 11)
	dBs.writeBytes(noePack("<BBIHBB", 1, 0, rootDirLba, 1, 0, 0))
	dBs.padToSizeFromCurrentOffset(beTableLba << 11)
	dBs.writeBytes(noePack(">BBIHBB", 1, 0, rootDirLba, 1, 0, 0))

	#root records
	dBs.padToSizeFromCurrentOffset(rootDirLba << 11)
	dBs.writeBytes(rootRecordData)

	#file data
	dBs.padToSizeFromCurrentOffset(firstDataLba << 11)
	dBs.writeBytes(fileData)
	
	dBs.padToSizeFromCurrentOffset(totalImageSize)
	
	return True
	
def writeDirectoryRecord(dBs, name, dataLba, dataSize):
	recordOffset = dBs.tell()
	currentLba = recordOffset >> 11

	isDots = 0
	if name == "." or name == "..":
		isDots = len(name)
		name = ""
		writeNameLen = 1
	else:
		name += ";1"
		writeNameLen = len(name)

	recordSize = (33 + writeNameLen + 1) & ~1

	recordData = bytearray(recordSize)
	recordData[0] = recordSize
	recordData[2 : 10] = dualEndianDW(dataLba)
	recordData[10 : 18] = dualEndianDW(dataSize)
	recordData[18] = DATE_YMD[0] - 1900 #fortunately, humans will have destroyed themselves by the year 2156
	recordData[19] = DATE_YMD[1]
	recordData[20] = DATE_YMD[2]
	recordData[25] = 2 if isDots else 0
	recordData[28 : 32] = dualEndianW(1)
	recordData[32] = writeNameLen

	recordData[33 : 33 + len(name)] = name.encode("ASCII")
	if isDots == 2:
		recordData[33] = 1
	
	endLba = (recordOffset + len(recordData)) >> 11
	
	if endLba != currentLba:
		recordOffset = endLba << 11
		dBs.padToSizeFromCurrentOffset(recordOffset)
	dBs.writeBytes(recordData)
	return recordOffset

def writeVolumeDate(dBs):
	dBs.writeBytes(("%04i"%DATE_YMD[0]).encode("ASCII"))
	dBs.writeBytes(("%02i"%DATE_YMD[1]).encode("ASCII"))
	dBs.writeBytes(("%02i"%DATE_YMD[2]).encode("ASCII"))
	dBs.writeBytes(b"00000000\0")
