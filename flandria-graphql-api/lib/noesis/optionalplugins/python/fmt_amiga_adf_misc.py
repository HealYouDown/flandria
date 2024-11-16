from inc_noesis import *
import os

ADF_SECTOR_SIZE = 512
ADF_FORCE_ROOT_BLOCK = 0 #880
ADF_USE_DIR_REF_AS_PARENT = False

ADF_FLAG_FFS = (1 << 0)
ADF_FLAG_INTL = (1 << 1)
ADF_FLAG_DIRC = (1 << 2)

ADF_BLOCKTYPE_ROOT = 1
ADF_BLOCKTYPE_DIR = 2
ADF_BLOCKTYPE_FILE = -3

ICO_DEFAULT_PALETTE = bytes(
	(
		0x00, 0x55, 0xAA,
		0xFF, 0xFF, 0xFF,
		0x00, 0x00, 0x00,
		0xFF, 0x88, 0x00,
		0x7B, 0x7B, 0x7B,
		0xAF, 0xAF, 0xAF,
		0xAA, 0x90, 0x7C,
		0xFF, 0xA9, 0x97
	)
)
ICO_DEFAULT_PALETTE_COUNT = len(ICO_DEFAULT_PALETTE) // 3
ICO_STRETCH = True
ICO_PAL0_TRANSPARENT = True

def registerNoesisTypes():
	handle = noesis.register("Amiga ADF Image", ".adf")
	noesis.setHandlerExtractArc(handle, adfExtractArc)
	
	handle = noesis.register("Amiga Icon", ".info")
	noesis.setHandlerTypeCheck(handle, icoCheckType)
	noesis.setHandlerLoadRGBA(handle, icoLoadRGBA)
	
	return 1

class IcoImage:
	def __init__(self, bs):
		self.x = bs.readShort()
		self.y = bs.readShort()
		self.width = bs.readUShort()
		self.height = bs.readUShort()
		self.bpp = bs.readUShort()
		self.hasImageData = bs.readUInt() != 0
		self.planePick = bs.readUByte()
		self.planeOnOff = bs.readUByte()
		self.nextImage = bs.readUInt()
		self.dataOffset = bs.tell()
		
	def calculateSize(self):
		padW = (((self.width + 15) & ~15) * self.bpp) // 8
		return padW * self.height
	
class IcoFile:
	def __init__(self, bs):
		self.bs = bs
		
	def parseHeader(self):
		bs = self.bs
		try:
			bs.setByteEndianForBits(NOE_BIGENDIAN)	
			self.id = bs.readUShort()
			self.ver = bs.readUShort()
			bs.readUInt()
			self.x = bs.readShort()
			self.y = bs.readShort()
			self.width = bs.readUShort()
			self.height = bs.readUShort()
			self.flags = bs.readUShort()
			bs.readShort()
			bs.readShort()
			self.hasImg0 = bs.readUInt() != 0
			self.hasImg1 = bs.readUInt() != 0
			if self.id != 0xE310 or self.ver != 1 or not self.hasImg0:
				return 0
			bs.seek(66, NOESEEK_ABS)
			drawerSize = 56 if bs.readUInt() != 0 else 0
			img0Offset = 78 + drawerSize
			
			bs.seek(img0Offset, NOESEEK_ABS)
			self.imgs = []
			img0 = IcoImage(bs)
			bs.seek(img0.calculateSize(), NOESEEK_REL)
			self.imgs.append(img0)
			if self.hasImg1:
				img1 = IcoImage(bs)
				#bs.seek(img1.calculateSize(), NOESEEK_REL)
				self.imgs.append(img1)
		except:
			return 0
		return 1
		
	def loadImages(self, texList):
		bs = self.bs
		for img in self.imgs:
			if not img.hasImageData:
				continue

			dstH = img.height * 2 if ICO_STRETCH else img.height
			
			padW = (img.width + 15) & ~15
			data = bytearray(img.width * img.height)
			bs.seek(img.dataOffset, NOESEEK_ABS)
			for planeIndex in range(img.bpp):
				for y in range(img.height):
					for x in range(img.width):
						d = y * img.width + x
						data[d] |= (bs.readBits(1) << planeIndex)
					bs.readBits(padW - img.width)

			rgba = bytearray(img.width * dstH * 4)
			for y in range(dstH):
				srcY = y >> 1 if ICO_STRETCH else y
				for x in range(img.width):
					pix = data[srcY * img.width + x]
					palOffset = pix * 3 if pix < ICO_DEFAULT_PALETTE_COUNT else 0
					palEntry = ICO_DEFAULT_PALETTE[palOffset : palOffset + 3]
					rgbaOffset = (y * img.width + x) * 4
					rgba[rgbaOffset : rgbaOffset + 3] = palEntry
					rgba[rgbaOffset + 3] = 255 if pix > 0 or not ICO_PAL0_TRANSPARENT else 0

			texList.append(NoeTexture("infoimg%04i"%len(texList), img.width, dstH, rgba, noesis.NOESISTEX_RGBA32))
	
def icoCheckType(data):
	ico = IcoFile(NoeBitStream(data, NOE_BIGENDIAN))
	return 1 if ico.parseHeader() else 0

def icoLoadRGBA(data, texList):
	ico = IcoFile(NoeBitStream(data, NOE_BIGENDIAN))
	ico.parseHeader()
	ico.loadImages(texList)
	return 1
	

class AdfTimeStamp:
	def __init__(self, bs):
		self.days = bs.readUInt()
		self.mins = bs.readUInt()
		self.ticks = bs.readUInt()
	
class AdfBlock:
	def __init__(self, bs):
		self.blockOffset = bs.tell()
		bs.seek(ADF_SECTOR_SIZE - 4, NOESEEK_REL)
		self.secType = bs.readInt()
		bs.seek(self.blockOffset, NOESEEK_ABS)
		
		self.fromDirIndex = -1
		self.type = bs.readUInt()
		self.headerKey = bs.readUInt()
		self.highSeq = bs.readUInt()
		self.htSize = bs.readUInt()
		self.firstData = bs.readUInt()
		self.checksum = bs.readUInt()
		dataTableSize = self.htSize if self.secType == ADF_BLOCKTYPE_ROOT else 72
		self.dataTable = [bs.readUInt() for x in range(dataTableSize)]
		if self.secType == ADF_BLOCKTYPE_ROOT:
			self.bmFlag = bs.readUInt()
			self.bmPages = [bs.readUInt() for x in range(25)]
			self.bmExt = bs.readUInt()
			self.rTime = AdfTimeStamp(bs)
		else:
			bs.readUInt()
			self.uid = bs.readUShort()
			self.gid = bs.readUShort()
			self.protect = bs.readUInt()
			self.fileSize = bs.readUInt()
			self.commSize = bs.readUByte()
			self.comm = bs.readBytes(79)
			bs.readBytes(12)
			self.time = AdfTimeStamp(bs)
		nameSize = bs.readUByte()
		nameData = bs.readBytes(30)[:nameSize]
		#possible todo - map non-ascii into appropriate amiga charset
		self.name = noeStrFromBytes(bytearray([x if x < 128 else ord("?") for x in nameData]))
		bs.readUByte() #unused
		bs.readUInt() #unused
		self.realEntry = bs.readUInt()
		if self.secType == ADF_BLOCKTYPE_ROOT:
			self.vTime = AdfTimeStamp(bs)
			self.cTime = AdfTimeStamp(bs)
			self.nextHash = bs.readUInt()
			self.parent = bs.readUInt()
			self.firstCacheBlock = bs.readUInt()
		else:
			self.nextLink = bs.readUInt()
			bs.readUInt() #unused
			bs.readUInt() #unused
			bs.readUInt() #unused
			bs.readUInt() #unused
			bs.readUInt() #unused
			self.nextHash = bs.readUInt()
			self.parent = bs.readUInt()
			self.fileExBlock = bs.readUInt()
		
class AdfBootBlock:
	def __init__(self, imageSize, bs):
		self.imageSize = imageSize
		self.bs = bs
		self.rootOffset = -1
		self.flags = bs.readUInt()
		if self.flags & 0xFFFFFF00 == 0x444F5300:
			self.checksum = bs.readUInt()
			self.rootSector = bs.readUInt()
			if ADF_FORCE_ROOT_BLOCK != 0:
				self.rootSector = ADF_FORCE_ROOT_BLOCK
			elif self.rootSector == 0 or (self.rootSector * ADF_SECTOR_SIZE) >= imageSize: #well then, just guess
				self.rootSector = 880
			self.rootOffset = ADF_SECTOR_SIZE * self.rootSector

	def isValid(self):
		return self.rootOffset > 0 and self.rootOffset < self.imageSize
		
	def buildRecursivePath(self, block):
		parentIndex = block.fromDirIndex if ADF_USE_DIR_REF_AS_PARENT else block.parent
		parentPath = self.buildRecursivePath(self.blockDict[parentIndex]) + "/" if parentIndex in self.blockDict else ""
		return parentPath + block.name

	def addFileRecursive(self, blockIndex):
		if blockIndex != 0 and blockIndex not in self.blockDict:
			bs = self.bs
			bs.seek(blockIndex * ADF_SECTOR_SIZE, NOESEEK_ABS)
			block = AdfBlock(bs)
			self.blockDict[blockIndex] = block
			self.addFileRecursive(block.nextHash)
			if block.secType == ADF_BLOCKTYPE_DIR:
				for childIndex in block.dataTable:
					self.addFileRecursive(childIndex)
					if childIndex != 0:
						self.blockDict[childIndex].fromDirIndex = blockIndex
		
	def parseFileSystem(self):
		bs = self.bs
		bs.seek(self.rootOffset, NOESEEK_ABS)
		rootBlock = AdfBlock(bs)
		self.blockDict = {}
		for blockIndex in rootBlock.dataTable:
			self.addFileRecursive(blockIndex)
				
	def extractFiles(self):
		bs = self.bs
		for block in self.blockDict.values():
			if block.secType == ADF_BLOCKTYPE_FILE:
				path = self.buildRecursivePath(block)
				
				data = bytearray()
				fileBlock = block
				while len(data) < block.fileSize:
					dataCount = len(fileBlock.dataTable)
					for dbIndex in range(dataCount):
						dbOffset = fileBlock.dataTable[dataCount - dbIndex - 1] * ADF_SECTOR_SIZE
						if dbOffset > 0:
							dataOffset = 0 if self.flags & ADF_FLAG_FFS else 24
							bs.seek(dbOffset + dataOffset, NOESEEK_ABS)
							data += bs.readBytes(ADF_SECTOR_SIZE - dataOffset)
					if not fileBlock.fileExBlock:
						break
					bs.seek(fileBlock.fileExBlock * ADF_SECTOR_SIZE, NOESEEK_ABS)
					fileBlock = AdfBlock(bs)
						
				print("Writing", path)
				if block.fileSize > len(data):
					print("Error: Couldn't read enough data for file:", len(data), "vs", block.fileSize)
				else:
					data = data[:block.fileSize]
				rapi.exportArchiveFile(path, data)

def adfExtractArc(fileName, fileLen, justChecking):
	if fileLen <= ADF_SECTOR_SIZE:
		return 0
		
	with open(fileName, "rb") as f:
		bs = NoeFileStream(f, NOE_BIGENDIAN)
		try:
			bb = AdfBootBlock(fileLen, bs)
			if not bb.isValid():
				return 0
			bb.parseFileSystem()
		except:
			return 0

		if justChecking:
			return 1
		
		bb.extractFiles()
		
	return 1
