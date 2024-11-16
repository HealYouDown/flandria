from inc_noesis import *

FLEX_DATA_TYPE_SHAPE = 0
FLEX_DATA_TYPE_FONT = 1
FLEX_DATA_TYPE_GUMP = 2

SHAPE_CANVAS_WIDTH = 320
SHAPE_CANVAS_HEIGHT = 200
SHAPE_PIXEL_SIZE = 2

#although this script is named after Ultima VIII, the Crusader games are also supported.

def registerNoesisTypes():
	handle = noesis.register("Ultima VIII Archive", ".flx")
	noesis.setHandlerExtractArc(handle, flexExtractArc)
	
	handle = noesis.register("Ultima VIII Shape", ".flex_shp;.flex_sh2")
	noesis.setHandlerTypeCheck(handle, lambda data: flexShapeCheckType(data, FLEX_DATA_TYPE_SHAPE))
	noesis.setHandlerLoadRGBA(handle, lambda data, texList: flexShapeLoadRgba(data, texList, FLEX_DATA_TYPE_SHAPE))
	noesis.addOption(handle, "-u8shpaspectcor", "resizes up to intended aspect ratio.", 0)	
	noesis.addOption(handle, "-u8shpdrawcanv", "render shapes to canvas.", 0)	
	
	handle = noesis.register("Ultima VIII Font", ".flex_fnt;.flex_fn2")
	noesis.setHandlerTypeCheck(handle, lambda data: flexShapeCheckType(data, FLEX_DATA_TYPE_FONT))
	noesis.setHandlerLoadRGBA(handle, lambda data, texList: flexShapeLoadRgba(data, texList, FLEX_DATA_TYPE_FONT))
	handle = noesis.register("Ultima VIII Gump", ".flex_gmp;.flex_gm2")
	noesis.setHandlerTypeCheck(handle, lambda data: flexShapeCheckType(data, FLEX_DATA_TYPE_GUMP))
	noesis.setHandlerLoadRGBA(handle, lambda data, texList: flexShapeLoadRgba(data, texList, FLEX_DATA_TYPE_GUMP))

	handle = noesis.register("Ultima VIII Glob", ".flex_glb")
	noesis.setHandlerTypeCheck(handle, flexGlobCheckType)
	noesis.setHandlerLoadRGBA(handle, flexGlobLoadRgba)
	
	return 0


class SkipIndexHeader:
	def __init__(self, bs, ver):
		self.offset = bs.readUInt() & 0xFFFFFF
		self.size = bs.readUShort() if ver < 2 else bs.readUInt()


class FrameHeader:
	def __init__(self, bs, ver, dataType, size):
		self.offset = bs.tell()
		self.dataSize = size
		if ver >= 2 and dataType != FLEX_DATA_TYPE_SHAPE:
			self.type = self.frame = self.diskPos = 0
		else:
			self.type = bs.readUShort()
			self.frame = bs.readUShort()
			self.diskPos = bs.readUInt()
		#SkipShapeData
		self.flags = bs.readUShort() if ver < 2 else bs.readUInt()
		self.w = bs.readUShort() if ver < 2 else bs.readUInt()
		self.h = bs.readUShort() if ver < 2 else bs.readUInt()
		self.hotX = bs.readShort() if ver < 2 else bs.readInt()
		self.hotY = bs.readShort() if ver < 2 else bs.readInt()
		self.dataOffset = bs.tell()


class Shape:
	def __init__(self, data, dataType, ver = -1):
		self.data = data
		self.dataType = dataType
		bs = NoeBitStream(data)
		#i usually try to avoid terrible crap like this, but am feeling a bit too lazy to accomplish it through analysis
		if ver < 0:
			ver = 2 if rapi.getLastCheckedName().endswith("2") else 1
		self.ver = ver
		self.frames = []
		self.maxX = bs.readUShort()
		self.maxY = bs.readUShort()
		frameCount = bs.readUShort()
		siHeaders = []
		for siIndex in range(frameCount):
			siHeaders.append(SkipIndexHeader(bs, self.ver))
		for siHeader in siHeaders:
			bs.seek(siHeader.offset, NOESEEK_ABS)
			self.frames.append(FrameHeader(bs, self.ver, dataType, siHeader.size))
			
	def decodeFrame(self, palData, frameIndex):
		if frameIndex < 0 or frameIndex >= len(self.frames):
			return None
		frameHeader = self.frames[frameIndex]
		frameData = self.data[frameHeader.dataOffset : frameHeader.dataOffset + frameHeader.dataSize]
		return rapi.callExtensionMethod("u8_decode_shape_frame", self.ver, frameData, palData, frameHeader.w, frameHeader.h, frameHeader.flags, 0)		


class GlobNode:
	def __init__(self, bs, typeData, ver):
		self.pos = (bs.readUByte() << 1, bs.readUByte() << 1, bs.readUByte())
		self.shapeIndex = bs.readUShort()
		self.frameIndex = bs.readUByte()
		typeEntrySize = flexTypeEntrySize(ver)
		typeOffset = self.shapeIndex * typeEntrySize
		flags = noeUnpack("<Q", typeData[typeOffset : typeOffset + 8])[0]
		self.typeFlags = flags & 4095
		self.family = (flags >> 12) & 15
		footpadOffset = 21 if ver >= 2 else 20
		footpadBitCount = 5 if ver >= 2 else 4
		footpadMask = (1 << footpadBitCount) - 1
		self.footpadX = (flags >> footpadOffset) & footpadMask
		footpadOffset += footpadBitCount
		self.footpadY = (flags >> footpadOffset) & footpadMask
		footpadOffset += footpadBitCount
		self.footpadZ = (flags >> footpadOffset) & footpadMask
		self.fgFlag = 0 if ver >= 2 else (flags >> 46) & 1 #possible todo - confirm fg flag for crusader
		
		fXyz = self.getFootpad(True)
		self.posEx = (self.pos[0] - fXyz[0], self.pos[1] - fXyz[1], self.pos[2] + fXyz[2])
		self.pY = self.pos[0] + self.pos[1]
		self.pExY = self.posEx[0] + self.posEx[1]
			
	def isFixed(self):
		return (self.typeFlags & 1) != 0
		
	def isForeground(self):
		return self.fgFlag != 0
			
	def getFootpad(self, isWorld):
		xyShift = 5 if isWorld else 3
		z = self.footpadZ << 3
		if z == 0 and not self.isFixed():
			z = 1		
		return (self.footpadX << xyShift, self.footpadY << xyShift, z)

	def getScreenCoords(self, camH, camV):
		return (
			((self.pos[0] - self.pos[1]) >> SHAPE_PIXEL_SIZE) - camH,
			((self.pos[0] + self.pos[1]) >> (SHAPE_PIXEL_SIZE + 1)) - self.pos[2] - camV
		)

	def getShapeKey(self):
		return self.shapeIndex | (self.frameIndex << 16)

	def Compare(a, b):
		#possible todo - this is a bunch of nonsense, follow game logic and employ flags
		if a.posEx[2] <= b.pos[2]:
			return -1
		if a.pos[2] >= b.posEx[2]:
			return 1
		if a.pos[2] == b.pos[2]:
			if a.pY == b.pY:
				if a.pExY == b.pExY:
					fA, _ = a.drawData
					fB, _ = b.drawData
					if fA.h == fB.h:
						if a.shapeIndex == b.shapeIndex:
							a.frameIndex - b.frameIndex
						return a.shapeIndex - b.shapeIndex
					return fA.h - fB.h
				return a.pExY - b.pExY
			return a.pY - b.pY
		return a.pos[2] - b.pos[2]


class FlexArchive:
	def __init__(self, fileName):
		self.isValid = False
		self.file = None
		try:
			self.fileName = fileName
			f = self.file = open(fileName, "rb")
			bs = NoeBitStream(f.read(128))
			headerLabel = bs.readBytes(81)
			if headerLabel[16:] != bytes([0x1A] * 65):
				return
			self.controlZ = bs.readUByte()
			bs.readUShort() #reserved
			self.indexCount = bs.readInt()
			self.ver = bs.readInt()
			self.size = bs.readUInt()
			self.checksum = bs.readUInt()
			if (self.ver != 1 and self.ver != 0xCD) or self.indexCount <= 0:
				return
			self.isValid = True
		except:
			pass
			
	def __del__(self):
		if self.file:
			self.file.close()
			self.file = None
			
	def __enter__(self):
		return self
		
	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def readIndex(self):
		#lazy way of identifying data that works with both u8 and crusader
		lf = rapi.getLocalFileName(self.fileName).lower()
		isU8 = lf.startswith("u8") #terrible hack to identify v2 shape files from crusader (only applicable for fonts/gumps/shapes)
		nameToExt = (
			("damage", "dmg"),
			("dtable", "dtb"),
			("usecode", "scr"),
			("font", "fnt" if isU8 else "fn2"),
			("glob", "glb"),
			("gump", "gmp" if isU8 else "gm2"),
			("shape", "shp" if isU8 else "sh2"),
			("sound", "snd"),
			("music", "mus")
		)
		self.fileExt = ".flex_bin"
		for nameSub, ext in nameToExt:
			if nameSub in lf:
				self.fileExt = ".flex_" + ext
		
		f = self.file
		bs = NoeBitStream(f.read(8 * self.indexCount))
		self.entries = []
		self.refIndexMap = {}
		for fileIndex in range(self.indexCount):
			offset = bs.readUInt()
			size = bs.readUInt()
			if offset > 0 and size > 0:
				self.refIndexMap[fileIndex] = len(self.entries)
				self.entries.append((fileIndex, offset, size))

	def readFile(self, fileIndex):
		f = self.file
		index, offset, size = self.entries[fileIndex]
		f.seek(offset, os.SEEK_SET)
		data = f.read(size)
		name = "file_%04i"%index + self.fileExt
		return name, data
		
	def readFileByReferenceIndex(self, refIndex):
		if refIndex not in self.refIndexMap:
			return "", bytearray(0)
		return self.readFile(self.refIndexMap[refIndex])


def flexFindPairedFile(fileName, returnPath = False):
	basePath = rapi.getDirForFilePath(rapi.getLastCheckedName())
	fullPath = os.path.join(basePath, fileName)
	foundPath = os.path.exists(fullPath)
	if not foundPath:
		fullPath = os.path.abspath(os.path.join(basePath, "..\\" + fileName))
		foundPath = os.path.exists(fullPath)

	if foundPath:
		if returnPath:
			return fullPath
		else:
			with open(fullPath, "rb") as f:
				return f.read()

	return None


def flexFindPalette():
	palNames = ("GAMEPAL.PAL", "U8PAL.PAL")
	basePath = rapi.getDirForFilePath(rapi.getLastCheckedName())
	foundPalPath = None
	for palName in palNames:
		palData = flexFindPairedFile(palName)
		if palData:
			break

	if not palData:
		palData = rapi.loadPairedFile("Ultima VIII Palette", ".pal")
		
	if palData:
		palDataSize = len(palData)
		if palDataSize > 768:
			palData = palData[palDataSize - 768:]
		palData = rapi.imageShiftUpTo8(palData, 256, 1, 3, 2)
	else:
		print("Warning: Failed to load palette data, creating a default greyscale palette.")
		palData = bytearray([x // 3 for x in range(768)])
	return palData


def flexCorrectAspectRatio(frameRgba, w, h):
	if noesis.optWasInvoked("-u8shpaspectcor"):
		newW = w * 5
		newH = h * 6
		frameRgba = rapi.imageResampleNearest(frameRgba, w, h, newW, newH)
		w = newW
		h = newH
	return frameRgba, w, h


def flexTypeEntrySize(ver):
	return 9 if ver >= 2 else 8


def flexShapeCheckType(data, dataType):
	try:
		shp = Shape(data, dataType)
		if len(shp.frames) == 0:
			return 0
	except:
		return 0
	return 1


def flexShapeLoadRgba(data, texList, dataType):
	shp = Shape(data, dataType)
	
	palData = flexFindPalette()
	
	for frameIndex in range(len(shp.frames)):
		frameHeader = shp.frames[frameIndex]
		if frameHeader.w == 1 and frameHeader.h == 1:
			continue

		name = "u8_shape_frame%03i"%frameIndex
		w = frameHeader.w
		h = frameHeader.h
		frameRgba = shp.decodeFrame(palData, frameIndex)

		if noesis.optWasInvoked("-u8shpdrawcanv"):
			canvasRgba = bytearray(SHAPE_CANVAS_WIDTH * SHAPE_CANVAS_HEIGHT * 4)
			posX = SHAPE_CANVAS_WIDTH // 2 - frameHeader.hotX
			posY = SHAPE_CANVAS_HEIGHT // 2 - frameHeader.hotY
			rapi.imageBlit32(canvasRgba, SHAPE_CANVAS_WIDTH, SHAPE_CANVAS_HEIGHT, posX, posY, frameRgba, w, h, 0, 0, 0, 0, noesis.BLITFLAG_ALPHABLEND | noesis.BLITFLAG_ALLOWCLIP)
			w = SHAPE_CANVAS_WIDTH
			h = SHAPE_CANVAS_HEIGHT
			frameRgba = canvasRgba

		frameRgba, w, h = flexCorrectAspectRatio(frameRgba, w, h)

		tex = NoeTexture(name, w, h, frameRgba, noesis.NOESISTEX_RGBA32)
		texList.append(tex)
	return 1


def flexGlobCheckType(data):
	if len(data) < 2:
		return 0
	nodeCount = noeUnpack("<H", data[:2])[0]
	if len(data) != 2 + nodeCount * 6:
		return 0
	return 1


def flexGlobLoadRgba(data, texList):
	bs = NoeBitStream(data)
	nodeCount = bs.readUShort()
	if nodeCount == 0:
		print("This glob contains no nodes.")
	else:
		typeData = flexFindPairedFile("TYPEFLAG.DAT")
		if not typeData:
			print("TYPEFLAG.DAT is required for glob rendering.")
		else:
			ver = 1
			flxPath = flexFindPairedFile("U8SHAPES.FLX", True)
			if not flxPath:
				ver = 2
				flxPath = flexFindPairedFile("SHAPES.FLX", True)
				
			if not flxPath:
				print("Can't load glob without shapes data.")
			else:
				with FlexArchive(flxPath) as flx:
					flx.readIndex()
					entryCount = flx.indexCount
					typeEntrySize = len(typeData) // entryCount
					if flexTypeEntrySize(ver) != typeEntrySize:
						print("Unexpected type entry size:", typeEntrySize)
					else:
						palData = flexFindPalette()
						shapeDict = {}
						frameDict = {}
						
						camH = camV = 0
						minX = minY = 1024 * 1024 * 1024
						maxX = maxY = -minX
						
						drawNodes = []
						for nodeIndex in range(nodeCount):
							node = GlobNode(bs, typeData, ver)
							if node.shapeIndex not in shapeDict:
								shapeData = flx.readFileByReferenceIndex(node.shapeIndex)[1]
								if not shapeData:
									print("Warning: Invalid shape index on node", nodeIndex)
									continue
								shapeDict[node.shapeIndex] = Shape(shapeData, FLEX_DATA_TYPE_SHAPE, ver)
								
							shapeKey = node.getShapeKey()
							if shapeKey not in frameDict:
								shape = shapeDict[node.shapeIndex]
								frameDict[shapeKey] = shape.decodeFrame(palData, node.frameIndex)
								
							frameData = frameDict.get(shapeKey)
							if frameData:
								frameHeader = shapeDict[node.shapeIndex].frames[node.frameIndex]
								x, y = node.getScreenCoords(camH, camV)
								x -= frameHeader.hotX
								y -= frameHeader.hotY
								maxX = max(maxX, x + frameHeader.w)
								maxY = max(maxY, y + frameHeader.h)
								minX = min(minX, x)
								minY = min(minY, y)
								node.drawX = x
								node.drawY = y
								node.drawData = (frameHeader, frameData)
								drawNodes.append(node)
							
						if len(drawNodes) > 0:
							drawNodes = sorted(drawNodes, key=noeCmpToKey(GlobNode.Compare))
							canvasWidth = maxX - minX
							canvasHeight = maxY - minY
							canvasRgba = bytearray(canvasWidth * canvasHeight * 4)
							for node in drawNodes:
								frameHeader, frameRgba = node.drawData
								rapi.imageBlit32(canvasRgba, canvasWidth, canvasHeight, node.drawX - minX, node.drawY - minY, frameRgba, frameHeader.w, frameHeader.h, 0, 0, 0, 0, noesis.BLITFLAG_ALPHABLEND | noesis.BLITFLAG_ALLOWCLIP)
								
							canvasRgba, canvasWidth, canvasHeight = flexCorrectAspectRatio(canvasRgba, canvasWidth, canvasHeight)

							tex = NoeTexture("u8glob", canvasWidth, canvasHeight, canvasRgba, noesis.NOESISTEX_RGBA32)
							texList.append(tex)
							return 1								
	return 0


def flexExtractArc(fileName, fileLen, justChecking):
	if fileLen < 128:
		return 0
	with FlexArchive(fileName) as flx:
		if not flx.isValid:
			return 0
		if justChecking:
			return 1
			
		flx.readIndex()

		for fileIndex in range(len(flx.entries)):
			name, data = flx.readFile(fileIndex)
			print("Writing", name)
			rapi.exportArchiveFile(name, data)
		
		return 1
