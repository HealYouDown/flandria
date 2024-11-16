from inc_noesis import *
from chunk import Chunk
from inc_adpcm import decodeSectorPSXCDXA, decodeBlockPSXSPU, getSectorInfoPSXCDXA
import os

SECTOR_SIZE = 2352

MAX_VIDEO_DIMENSION = 0x1000 #not a hard limit, just here to sanity-check

#handling of ADPCM and video streams works both ways. this script will auto-extract the audio from a video if you give it an extension of .xa.
#the video implementation is barebones and was written with only Bushido Blade as a reference, but should still work with plenty of other games.

def registerNoesisTypes():
	handle = noesis.register("PSX CD-XA Audio", ".xa;.xai")
	noesis.setHandlerExtractArc(handle, xaAdpcmExtractArc)
	
	handle = noesis.register("PSX CD-XA Video", ".str;.stx")
	noesis.setHandlerTypeCheck(handle, xaVideoStreamCheckType)
	noesis.setHandlerLoadRGBA(handle, xaVideoStreamLoadRgba)
	
	return 1


def getCdxaRiffHeaderSize(bs, fileLen):
	riffHeaderSize = 0
	try:
		#see if it's got a riff header.
		#some tools (and Windows) like to slap this in front of files beginning with audio sectors. we could potentially use it for validation, but we don't need it.
		riffChunk = Chunk(bs, bigendian=False)
		if riffChunk.chunkname == b"RIFF" and bs.readBytes(4) == b"CDXA":
			fmtChunk = Chunk(bs, bigendian=False)
			if fmtChunk.chunkname == b"fmt ":
				fmtChunk.skip()
				dataChunk = Chunk(bs, bigendian=False)
				if dataChunk.chunkname == b"data":
					riffHeaderSize = bs.tell()
	except:
		pass
	
	if (riffHeaderSize + SECTOR_SIZE) > fileLen:
		return -1

	bs.seek(riffHeaderSize, NOESEEK_ABS)
	xaHeaderData = bs.read(24)
	#do some weak mode2 header validation
	if xaHeaderData[:12] != bytes((0x00, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0x00)) or xaHeaderData[16:20] != xaHeaderData[20:24]:
		return -1
	
	return riffHeaderSize

	
def xaAdpcmExtractArc(fileName, fileLen, justChecking):
	if fileLen < SECTOR_SIZE:
		return 0
	with open(fileName, "rb") as f:
		bs = NoeBitStream(f.read(SECTOR_SIZE))
		riffHeaderSize = getCdxaRiffHeaderSize(bs, fileLen)
		if riffHeaderSize < 0:
			return 0

		if justChecking:
			return 1

		f.seek(riffHeaderSize, os.SEEK_SET)
		sectorCount = (fileLen - riffHeaderSize) // SECTOR_SIZE
		
		channelStreams = {}
		try:
			for sectorIndex in range(sectorCount):
				if (sectorIndex & 2047) == 0:
					print("Processing sector", sectorIndex, "/", sectorCount)			
				sectorData = f.read(SECTOR_SIZE)
				if not sectorData[18] & 4:
					#not an audio sector
					continue
				channelNum, isStereo, sampleRate, bps = getSectorInfoPSXCDXA(sectorData)
				if channelNum not in channelStreams:
					fileName = "xa_dump_%i.wav"%channelNum
					print("Beginning stream for", fileName)
					fullPath = rapi.exportArchiveFileGetName(fileName)
					fw = open(fullPath, "wb")
					#we'll come around and fix up the size in the header after we're done writing
					waveHeader = rapi.createPCMWaveHeader(666, 16, sampleRate, 2 if isStereo else 1)
					fw.write(waveHeader)
					channelStreams[channelNum] = fw, waveHeader, isStereo, sampleRate, bps, [0.0, 0.0], [0.0, 0.0]
				#this is slow as shit, should probably move more of the decoding to native land. this would be very threadable too.
				channelStream, _, _, _, _, oldSamplesLeft, oldSamplesRight = channelStreams[channelNum]
				channelStream.write(decodeSectorPSXCDXA(sectorData, oldSamplesLeft, oldSamplesRight))
		except:
			print("Encountered an exception during ADPCM decoding.")

		print("Finalizing streams.")
		for channelNum in channelStreams.keys():
			channelStream, waveHeader, _, _, _, _, _ = channelStreams[channelNum]
			finalSize = channelStream.tell() - len(waveHeader)
			#fix up the sizes in the header
			channelStream.seek(4, os.SEEK_SET)
			channelStream.write(noePack("<I", finalSize + len(waveHeader) - 8))
			channelStream.seek(len(waveHeader) - 4, os.SEEK_SET)
			channelStream.write(noePack("<I", finalSize))
			channelStream.close()

	return 1


class StandardVideoFrameSectorHeader:
	def __init__(self, bs, sectorIndex):
		self.headerOffset = bs.tell()
		self.absSectorIndex = sectorIndex
		self.cmd = bs.readUInt() #BB adds in 0x2000000 at runtime - binary can't be trusted to determine alpha fill
		self.sectorIndex = bs.readUShort()
		self.sectorCount = bs.readUShort()
		self.frameIndex = bs.readInt()
		self.frameSize = bs.readInt()
		self.width = bs.readUShort()
		self.height = bs.readUShort()
		self.mdcCount = bs.readUShort()
		self.id = bs.readUShort()
		self.quantScale = bs.readUShort()
		self.ver = bs.readUShort()
		self.resv1 = bs.readUInt()
		if self.ver <= 1:
			self.ver = 2
		self.dataOffset = bs.tell()
		self.dataSize = 2048 - (self.dataOffset - self.headerOffset)

	def isValid(self):
		validId = (self.cmd == 0x80010160) or (self.id == 0x3800 and self.ver >= 2 and self.ver <= 3)
		return validId and self.width > 0 and self.width <= MAX_VIDEO_DIMENSION and self.height > 0 and self.height <= MAX_VIDEO_DIMENSION


class StandardVideoFrameHeader:
	def __init__(self, bs):
		self.expectedDataSize = bs.readUShort()
		self.id = bs.readUShort()
		self.quantScale = bs.readUShort()
		self.ver = bs.readUShort()
		if self.ver <= 1:
			self.ver = 2
		self.dataOffset = bs.tell()
		
	def isValid(self):
		return self.id == 0x3800 and self.ver >= 2 and self.ver <= 3


def xaVideoStreamCheckType(data):
	return 0 if getCdxaRiffHeaderSize(NoeBitStream(data), len(data)) < 0 else 1


def xaVideoStreamLoadRgba(data, texList):
	bs = NoeBitStream(data)
	riffHeaderSize = getCdxaRiffHeaderSize(bs, len(data))
	
	print("Scanning for video sectors.")
	
	sectorCount = (len(data) - riffHeaderSize) // SECTOR_SIZE
	bs.seek(riffHeaderSize, NOESEEK_ABS)
	videoFrameSectors = []
	for sectorIndex in range(sectorCount):
		sectorData = bs.readBytes(SECTOR_SIZE)
		if not (sectorData[18] & 10) or (sectorData[18] & 4):
			#not a video/data sector
			continue
		secBs = NoeBitStream(sectorData)
		secBs.seek(24, NOESEEK_ABS)
		frameSectorHeader = StandardVideoFrameSectorHeader(secBs, sectorIndex)
		if not frameSectorHeader.isValid():
			continue
		videoFrameSectors.append((frameSectorHeader, secBs.readBytes(frameSectorHeader.dataSize)))

	baseTexIndex = len(texList)
	if len(videoFrameSectors) > 0:
		#BB $8008f984 - part of libpress. since BB uses the default matrix, we pass None instead.
		#this will cause the Noesis MDEC implementation to calculate its own IDCT matrix and perform high-precision transforms.
		"""
		idctData = bytes((
			0x82, 0x5A, 0x82, 0x5A, 0x82, 0x5A, 0x82, 0x5A, 0x82, 0x5A, 0x82, 0x5A, 0x82, 0x5A, 0x82, 0x5A,
			0x8A, 0x7D, 0x6D, 0x6A, 0x1C, 0x47, 0xF8, 0x18, 0x07, 0xE7, 0xE3, 0xB8, 0x92, 0x95, 0x75, 0x82,
			0x41, 0x76, 0xFB, 0x30, 0x04, 0xCF, 0xBE, 0x89, 0xBE, 0x89, 0x04, 0xCF, 0xFB, 0x30, 0x41, 0x76,
			0x6D, 0x6A, 0x07, 0xE7, 0x75, 0x82, 0xE3, 0xB8, 0x1C, 0x47, 0x8A, 0x7D, 0xF8, 0x18, 0x92, 0x95,
			0x82, 0x5A, 0x7D, 0xA5, 0x7D, 0xA5, 0x82, 0x5A, 0x82, 0x5A, 0x7D, 0xA5, 0x7D, 0xA5, 0x82, 0x5A,
			0x1C, 0x47, 0x75, 0x82, 0xF8, 0x18, 0x6D, 0x6A, 0x92, 0x95, 0x07, 0xE7, 0x8A, 0x7D, 0xE3, 0xB8,
			0xFB, 0x30, 0xBE, 0x89, 0x41, 0x76, 0x04, 0xCF, 0x04, 0xCF, 0x41, 0x76, 0xBE, 0x89, 0xFB, 0x30,
			0xF8, 0x18, 0xE3, 0xB8, 0x6D, 0x6A, 0x75, 0x82, 0x8A, 0x7D, 0x92, 0x95, 0x1C, 0x47, 0x07, 0xE7
		))
		"""
		idctData = None
		
		qScaleYData = bytes((
			#BB $8008f900 - part of libpress
			0x02, 0x10, 0x10, 0x13, 0x10, 0x13, 0x16, 0x16,
			0x16, 0x16, 0x16, 0x16, 0x1A, 0x18, 0x1A, 0x1B,
			0x1B, 0x1B, 0x1A, 0x1A, 0x1A, 0x1A, 0x1B, 0x1B,
			0x1B, 0x1D, 0x1D, 0x1D, 0x22, 0x22, 0x22, 0x1D,
			0x1D, 0x1D, 0x1B, 0x1B, 0x1D, 0x1D, 0x20, 0x20,
			0x22, 0x22, 0x25, 0x26, 0x25, 0x23, 0x23, 0x22,
			0x23, 0x26, 0x26, 0x28, 0x28, 0x28, 0x30, 0x30,
			0x2E, 0x2E, 0x38, 0x38, 0x3A, 0x45, 0x45, 0x53
		))
		qScaleCData = qScaleYData #BB $8008f940, actual values are identical to y
		
		#games generally shouldn't have frames/sectors out of order, but go ahead and enforce the order here anyway
		videoFrameSectors = sorted(videoFrameSectors, key=noeCmpToKey(lambda a,b: a[0].sectorIndex - b[0].sectorIndex if a[0].frameIndex == b[0].frameIndex else a[0].frameIndex - b[0].frameIndex))

		currentSectorIndex = 0
		while currentSectorIndex < len(videoFrameSectors):
			frameSectorHeader, _ = videoFrameSectors[currentSectorIndex]
			frameData = bytearray()
			for sectorIndex in range(frameSectorHeader.sectorCount):
				_, sectorData = videoFrameSectors[currentSectorIndex]
				frameData += sectorData
				currentSectorIndex += 1
			frameBs = NoeBitStream(frameData)
			frameHeader = StandardVideoFrameHeader(frameBs)
			if not frameHeader.isValid():
				#hack for ff7, try skipping 40 bytes in front
				frameBs.seek(40, NOESEEK_ABS)
				frameHeader = StandardVideoFrameHeader(frameBs)
				if not frameHeader.isValid():
					continue
		
			print("Decoding frame", frameSectorHeader.frameIndex)
			
			#implements BB $80078660, which decodes huffman-compressed block data into MDEC-readable data
			mdecData = rapi.imagePSXDecodeVideoFrame(frameData[frameHeader.dataOffset:], frameHeader.ver, frameSectorHeader.width, frameSectorHeader.height, frameHeader.quantScale)
			if not mdecData:
				print("Error: Failed to decode frame.")
				continue

			#renders blocks in column order. if you need to handle something custom, you can split the data to render one block at a time.
			rgbaData = rapi.imagePSXMDEC(mdecData, idctData, qScaleCData, qScaleYData, frameSectorHeader.width, frameSectorHeader.height)

			tex = NoeTexture("str_frame%04i"%frameSectorHeader.frameIndex, frameSectorHeader.width, frameSectorHeader.height, rgbaData, noesis.NOESISTEX_RGBA32)
			tex.setFrameInfo(frameSectorHeader.frameIndex, 1000.0 / 15.0) #default to 15 fps
			texList.append(tex)

	return 1 if len(texList) > baseTexIndex else 0
