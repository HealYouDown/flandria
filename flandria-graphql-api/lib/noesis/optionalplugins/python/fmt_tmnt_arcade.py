from inc_noesis import *
from inc_romcom import *

#K052109
TILE_WIDTH = 8
TILE_HEIGHT = 8
#K051960 and K053244
SPR_WIDTH = 16
SPR_HEIGHT = 16
SPR_MACRO_WIDTH = SPR_WIDTH * 8
SPR_MACRO_HEIGHT = SPR_HEIGHT * 8

BLOCK_WIDTH = TILE_WIDTH * 4
BLOCK_HEIGHT = TILE_HEIGHT * 4

SHADOW_ALPHA = 127

TMNT_LEVEL_COUNT = 10
TMNT2_LEVEL_COUNT = 9

PAL_SIZE = 16 * 2
PAL_SIZE_RGBA = PAL_SIZE * 2

LOAD_RAW = False
LOAD_SPRITES = True
LOAD_LEVELS = True

POINTER_TRAVERSAL_HACK = True #do some extra hackery to get extra frames during the automated traversal. may get extra junk in addition to valid data.
UNIQUE_FRAMES_ONLY = True #won't load duplicate sprite frames in cases where animations share frame pointers.
DRAW_TO_CANVAS = True #creates a canvas large enough to fit every object with correct offsets.


def registerNoesisTypes():
	handle = noesis.register("TMNT Arcade ROM", ".j17")
	noesis.setHandlerTypeCheck(handle, lambda data: 1 if rapi.lastCheckedPartialChecksum(0, 0x1000) == 0x2F23D0D5 else 0)
	noesis.setHandlerLoadRGBA(handle, tmntLoadRGBA)
	
	handle = noesis.register("TMNT:TiT Arcade ROM", ".8e")
	noesis.setHandlerTypeCheck(handle, lambda data: 1 if rapi.lastCheckedPartialChecksum(0, 0x1000) == 0x1F0C068C else 0)
	noesis.setHandlerLoadRGBA(handle, tmnt2LoadRGBA)
	
	return 0


def tmntReadImageSets(imageBasePath, imageSets, interleaveSize):
	data = bytearray()
	for imageSize, imageSet in imageSets:
		data += readRomImages(imageBasePath, imageSet, imageSize, ReadRomImageFlag_Interleave, False, interleaveSize)
	return data


#some of the bits in here were gleaned from BSD-3 MAME source

tmntTransformTileBits = lambda data: noesis.transformBitsArray(data, 4, bytearray((0, 4, 8, 12, 16, 20, 24, 28, 1, 5, 9, 13, 17, 21, 25, 29, 2, 6, 10, 14, 18, 22, 26, 30, 3, 7, 11, 15, 19, 23, 27, 31)))
	
#if i weren't already going to hell, this would do the trick
tmntInterleaveImagePlanes = lambda data: noesis.transformBitsArray(noesis.transformBitsArray(data, 4, bytearray([i for s in [(31 - r, 23 - r, 15 - r, 7 - r) for r in range(8)] for i in s])), 1, bytearray((3, 2, 1, 0, 7, 6, 5, 4)))

def tmntCreateSpritePages(data, isK053244):
	data = rapi.imageArrangeTiles(data, 1, TILE_WIDTH >> 1, TILE_HEIGHT, SPR_WIDTH >> 1, (0, 1, 2, 3))
	if isK053244:
		macroTileLUT = [i for i in range(64)]
	else:
		macroTileLUT = (
			0, 1, 4, 5, 16, 17, 20, 21,
			2, 3, 6, 7, 18, 19, 22, 23,
			8, 9, 12, 13, 24, 25, 28, 29,
			10, 11, 14, 15, 26, 27, 30, 31,
			32, 33, 36, 37, 48, 49, 52, 53,
			34, 35, 38, 39, 50, 51, 54, 55,
			40, 41, 44, 45, 56, 57, 60, 61,
			42, 43, 46, 47, 58, 59, 62, 63
		)
	return rapi.imageArrangeTiles(data, 1, SPR_WIDTH >> 1, SPR_HEIGHT, SPR_MACRO_WIDTH >> 1, macroTileLUT)


TMNT_SPR_SIZES = (
	(1, 1), (2, 1), (1, 2), (2, 2), (4, 2), (2, 4), (4, 4), (8, 8)
)

class TmntFramePart:
	def __init__(self, bs):
		self.attrs = a = [bs.readUByte() for _ in range(3)]
		self.flags = bs.readUByte()
		self.x = bs.readShort()
		self.y = -bs.readShort()
		self.sprSize = (a[0] & 0xE0) >> 5 #see also: $4716E
		self.sprIndex = a[1] | ((a[0] & 0x1F) << 8) | ((a[2] & 0x10) << 9)
		self.hasShadow = (a[2] & 0x80) != 0
		self.palOffset = (16 + (a[2] & 15)) << 6 #in rgba32 palette space
		self.mirrorFlags = 0
		xSize, ySize = TMNT_SPR_SIZES[self.sprSize]
		self.width = xSize * SPR_WIDTH
		self.height = ySize * SPR_HEIGHT
		pageOffsets = noesis.transformBits(self.sprIndex, bytearray((0, 2, 4, 1, 3, 5)))
		self.pageX = (pageOffsets & 7) * SPR_WIDTH
		self.pageY = (self.sprIndex >> 6) * SPR_MACRO_HEIGHT + (pageOffsets >> 3) * SPR_HEIGHT
		
	def getBounds(self):
		return (self.x, self.y, self.x + self.width, self.y + self.height)


class TmntFrame:
	def __init__(self, bs, partCount):
		self.offset = bs.tell()
		self.loadParts(bs, partCount)
		self.bounds = tmntGetBounds(self.parts)

	def loadParts(self, bs, partCount):
		self.parts = [TmntFramePart(bs) for _ in range(partCount)][::-1]
		
	def getBounds(self):
		return self.bounds


class TmntFrameSet:
	def __init__(self, bs, namePrefix, palAddr = -1):
		self.offset = bs.tell()
		self.palAddr = palAddr
		self.frames = []
		self.loadFrames(bs, namePrefix)
		if len(self.frames) > 0:
			self.bounds = tmntGetBounds(self.frames)
		
	def loadFrames(self, bs, namePrefix):
		nextOffset = bs.tell()
		while not bs.checkEOF():
			bs.seek(nextOffset, NOESEEK_ABS)
			animCmd = bs.readUByte()
			pcOrTerminator = bs.readUByte()
			if len(self.frames) > 0 and animCmd == 0:
				#see $4712E - if pcOrTerminator != 0, an explicit frame address follows - we break in this case, since it probably means a loop.
				#if it's 0, it means hold on the frame, in which case we also break, as no frames follow.
				break
			partCount = (pcOrTerminator & 0x7F) + 1
			partsOffset = bs.readUInt()
			if partsOffset >= bs.getSize():
				#hack for the frames that aren't frames which might make it to this point from the pointer traversing mess
				break
			u0 = bs.readUByte()
			u1 = bs.readUByte()
			dmgVel = bs.readShort()
			if dmgVel >= 0:
				#see $47254
				bs.seek(8, NOESEEK_REL)
			nextOffset = bs.tell()
			bs.seek(partsOffset, NOESEEK_ABS)
			frame = TmntFrame(bs, partCount)
			frame.name = namePrefix + "_set%06X_frame%02i"%(self.offset, len(self.frames))
			self.frames.append(frame)
		self.bounds = tmntGetBounds(self.frames)
			
	def getBounds(self):
		return self.bounds

		
def tmntGetBounds(objects):
	minX, minY, maxX, maxY = objects[0].getBounds()
	for partIndex in range(1, len(objects)):
		pminX, pminY, pmaxX, pmaxY = objects[partIndex].getBounds()
		minX = min(minX, pminX)
		minY = min(minY, pminY)
		maxX = max(maxX, pmaxX)
		maxY = max(maxY, pmaxY)
	return (minX, minY, maxX, maxY)
	
	
def tmntTraverseAddressList(bs, offset, stopAddr = -1):
	addrs = []
	minAddr = 0xFFFFFFFF
	bs.seek(offset, NOESEEK_ABS)
	while not bs.checkEOF():
		addr = bs.readUInt()
		if (addr & 0xFF000000) == 0xFF000000:
			break
		minAddr = min(minAddr, addr)
		if POINTER_TRAVERSAL_HACK and minAddr < offset:
			#hack for shredder and some other objects where frame data doesn't conveniently live right after the pointers
			if (addr & 0xF0000) != (offset & 0xF0000):
				break
			bs.pushOffset()
			bs.seek(addr + 2, NOESEEK_ABS)
			frameAddr = bs.readInt()
			bs.popOffset()
			if (frameAddr & 0xF0000) != (offset & 0xF0000):
				break
			
		if addr not in addrs:
			addrs.append(addr)
		if (not POINTER_TRAVERSAL_HACK or minAddr >= offset) and bs.tell() >= minAddr:
			break
		elif stopAddr >= 0 and bs.tell() >= stopAddr:
			break
	return addrs

def tmntFindFramesFromAnimList(bs, offset, frameSets, namePrefix, frameSetType, palAddr = -1, stopAddr = -1):
	frameAddrs = tmntTraverseAddressList(bs, offset, stopAddr)
	for frameAddr in frameAddrs:
		bs.seek(frameAddr, NOESEEK_ABS)
		fs = frameSetType(bs, namePrefix, palAddr)
		if len(fs.frames) > 0:
			frameSets.append(fs)

def tmntFindFramesFromMoveList(bs, offset, frameSets, namePrefix, frameSetType = TmntFrameSet):
	addrs = tmntTraverseAddressList(bs, offset)
	for addr in addrs:
		tmntFindFramesFromAnimList(bs, addr, frameSets, namePrefix, frameSetType)

def tmntFindFramesFromEnemyList(bs, offset, frameSets, frameSetType):
	bs.seek(offset, NOESEEK_ABS)
	animPalAddrs = []
	zeroCount = 0
	while not bs.checkEOF():
		animAddr = bs.readInt()
		bs.readInt()
		if animAddr <= 0:
			zeroCount += 1
			if zeroCount > 2:
				break
			continue
		else:
			zeroCount = 0
		animPalAddrs.append((animAddr, len(animPalAddrs)))

	for entryIndex in range(len(animPalAddrs)):
		animAddr, enemySetIndex = animPalAddrs[entryIndex]
		nextAddr = animPalAddrs[entryIndex + 1][0] if entryIndex + 1 < len(animPalAddrs) else -1
		
		bs.seek(animAddr, NOESEEK_ABS)
		fs = frameSetType(bs, "enemies_set%03i"%enemySetIndex, -1)
		if len(fs.frames) > 0:
			frameSets.append(fs)

def tmntFindFramesFromObjectList(bs, offset, frameSets):
	bs.seek(offset, NOESEEK_ABS)
	animPalAddrs = []
	while not bs.checkEOF():
		animAddr = bs.readInt()
		if animAddr < 0:
			break
		palAddr = bs.readInt()
		animPalAddrs.append((animAddr, palAddr, len(animPalAddrs)))

	if POINTER_TRAVERSAL_HACK:
		animPalAddrs = sorted(animPalAddrs, key=noeCmpToKey(lambda a,b: a[0] - b[0] if a[0] != b[0] else a[1] - b[1] if a[1] != b[1] else a[2] - b[2]))

	for entryIndex in range(len(animPalAddrs)):
		animAddr, palAddr, objIndex = animPalAddrs[entryIndex]
		nextAddr = animPalAddrs[entryIndex + 1][0] if entryIndex + 1 < len(animPalAddrs) else -1
		tmntFindFramesFromAnimList(bs, animAddr, frameSets, "object%03i"%objIndex, TmntFrameSet, palAddr, nextAddr if POINTER_TRAVERSAL_HACK else -1)


def tmntLoadPalettes(bs, palRgba, offset, listAddr, palCount):
	bs.seek(listAddr, NOESEEK_ABS)
	for palIndex in range(palCount):
		palAddr = bs.readUInt()
		bs.pushOffset()
		bs.seek(palAddr, NOESEEK_ABS)
		bankData = noesis.swapEndianArray(bs.readBytes(PAL_SIZE), 2)
		bs.popOffset()
		bankRgba = rapi.imageDecodeRaw(bankData, len(bankData) >> 1, 1, "r5g5b5p1")
		palOffset = offset + palIndex * PAL_SIZE_RGBA
		palRgba[palOffset : palOffset + PAL_SIZE_RGBA] = bankRgba


def tmntRenderFrameSets(bs, sprData, frameSets, palRgba, texList):
	sprData += bytearray((SPR_MACRO_WIDTH * SPR_MACRO_HEIGHT) >> 1)
	totalBounds = tmntGetBounds(frameSets)
	canvasWidth = totalBounds[2] - totalBounds[0]
	canvasHeight = totalBounds[3] - totalBounds[1]
	currentPalAddr = -1
	visitedFrames = set()
	for frameSet in frameSets:
		if frameSet.palAddr >= 0 and currentPalAddr != frameSet.palAddr:
			currentPalAddr = frameSet.palAddr
			bs.seek(frameSet.palAddr + 12, NOESEEK_ABS)
			palSetAddr = bs.readUInt()
			tmntLoadPalettes(bs, palRgba, 0x400, palSetAddr, 16)
		
		for frame in frameSet.frames:
			if UNIQUE_FRAMES_ONLY:
				if frame.offset in visitedFrames:
					continue
				visitedFrames.add(frame.offset)

			if not DRAW_TO_CANVAS:
				#refit canvas to every frame
				totalBounds = frame.getBounds()
				canvasWidth = totalBounds[2] - totalBounds[0]
				canvasHeight = totalBounds[3] - totalBounds[1]
			frameRgba = bytearray(canvasWidth * canvasHeight * 4)

			for part in frame.parts:
				x = part.x - totalBounds[0]
				y = part.y - totalBounds[1]
				palEntry = palRgba[part.palOffset : part.palOffset + PAL_SIZE_RGBA]
				palEntry[3] = 0
				if part.hasShadow:
					palEntry[PAL_SIZE_RGBA - 1] = SHADOW_ALPHA
				#decode the part with the full page stride, it'll be clipped in the blt
				partOffset = (part.pageY * SPR_MACRO_WIDTH + part.pageX) >> 1
				partData = sprData[partOffset : partOffset + ((SPR_MACRO_WIDTH * SPR_MACRO_HEIGHT) >> 1)]
				partRgba = rapi.imageDecodeRawPal(partData, palEntry, SPR_MACRO_WIDTH, part.height, 4, "r8g8b8a8")
				partStride = SPR_MACRO_WIDTH * 4

				if (part.flags & 192) or part.mirrorFlags:
					#clip it and flip (and/or mirror) it
					cpartRgba = bytearray(part.width * part.height * 4)
					rapi.imageBlit32(cpartRgba, part.width, part.height, 0, 0, partRgba, part.width, part.height, 0, 0, 0, partStride, 0)
					partRgba = cpartRgba
					partStride = part.width * 4
					if part.mirrorFlags & 1:
						halfWidth = part.width >> 1
						halfPartRgba = bytearray(halfWidth * part.height * 4)
						rapi.imageBlit32(halfPartRgba, halfWidth, part.height, 0, 0, partRgba, halfWidth, part.height, 0, 0, 0, partStride, 0)
						halfPartRgba = rapi.imageFlipRGBA32(halfPartRgba, halfWidth, part.height, 1, 0)
						rapi.imageBlit32(partRgba, part.width, part.height, halfWidth, 0, halfPartRgba, halfWidth, part.height, 0, 0, 0, 0, 0)
					if part.mirrorFlags & 2:
						halfHeight = part.height >> 1
						halfPartRgba = bytearray(part.width * halfHeight * 4)
						#mirror from the bottom
						rapi.imageBlit32(halfPartRgba, part.width, halfHeight, 0, 0, partRgba, part.width, halfHeight, 0, halfHeight, 0, 0, 0)
						halfPartRgba = rapi.imageFlipRGBA32(halfPartRgba, part.height, halfHeight, 0, 1)
						rapi.imageBlit32(partRgba, part.width, part.height, 0, 0, halfPartRgba, part.height, halfHeight, 0, 0, 0, 0, 0)
					if part.flags & 192:
						partRgba = rapi.imageFlipRGBA32(partRgba, part.width, part.height, 1 if (part.flags & 128) else 0, 1 if (part.flags & 64) else 0)

				rapi.imageBlit32(frameRgba, canvasWidth, canvasHeight, x, y, partRgba, part.width, part.height, 0, 0, 0, partStride, noesis.BLITFLAG_ALPHATEST | noesis.BLITFLAG_ALLOWCLIP)

			tex = NoeTexture(frame.name, canvasWidth, canvasHeight, frameRgba, noesis.NOESISTEX_RGBA32)
			tex.flags |= noesis.NTEXFLAG_FILTER_NEAREST | noesis.NTEXFLAG_WRAP_CLAMP
			texList.append(tex)


def tmntLoadSprites(codeData, sprData, texList):
	bs = NoeBitStream(codeData, NOE_BIGENDIAN)

	#we'll just grab the first level's sprite palette. not everything will look right, but i guess if you care, stick the address for the palette you want here!
	defaultPalListAddr = 0xBC48
	defaultPalCount = 16
	palRgba = bytearray(0x1000)
	#sprites don't reference anything below 0x400, so no need to populate it
	tmntLoadPalettes(bs, palRgba, 0x400, defaultPalListAddr, defaultPalCount)

	frameSets = []
	tmntFindFramesFromMoveList(bs, 0x208D0, frameSets, "leo")
	tmntFindFramesFromMoveList(bs, 0x231F8, frameSets, "mike")
	tmntFindFramesFromMoveList(bs, 0x25CD4, frameSets, "don")
	tmntFindFramesFromMoveList(bs, 0x2883E, frameSets, "raph")
	tmntFindFramesFromObjectList(bs, 0x085BC, frameSets)
	
	tmntRenderFrameSets(bs, sprData, frameSets, palRgba, texList)


class TmntMap:
	def __init__(self, scrollInfo, tileRefsAddr, tilesAddr, widthInfo, palBase, decodeFlags):
		#see $1E11E
		self.scrollInfo = scrollInfo
		self.tileRefsAddr = tileRefsAddr
		self.tilesAddr = tilesAddr
		self.widthInfo = widthInfo
		self.palBase = palBase
		self.decodeFlags = decodeFlags
		self.widthInBlocks = widthInfo >> 1
		self.heightInBlocks = (self.scrollInfo[1] & 0xFF) << 3
		self.layerIndex = 0

	def loadMap(self, bs):
		bs.seek(self.tileRefsAddr, NOESEEK_ABS)
		#implements $1E150 / $1E088 across entire map
		self.mapData = rapi.callExtensionMethod("tmnt_map_decode", bs.getBuffer(), self.tileRefsAddr, self.tilesAddr, self.widthInBlocks, self.heightInBlocks, self.decodeFlags)
		
	def drawTiles(self, tileData, palRgba, reg6B, reg6E, name, bs):
		widthInTiles = self.widthInBlocks * (BLOCK_WIDTH // TILE_WIDTH)
		heightInTiles = self.heightInBlocks * (BLOCK_HEIGHT // TILE_HEIGHT)
		width = widthInTiles * TILE_WIDTH
		height = heightInTiles * TILE_HEIGHT
		tileInfo = noeUnpack("<" + "H" * (len(self.mapData) >> 1), self.mapData) #intentionally unpack as little, draw function expects info in big
		rgba = bytearray(width * height * 4)
		for tileIndex in range(len(tileInfo)):
			rapi.imageK052109DrawTile(rgba, width, height, (tileIndex % widthInTiles) * TILE_WIDTH, (tileIndex // widthInTiles) * TILE_HEIGHT, tileInfo[tileIndex], tileData, palRgba[self.palBase:], reg6B, reg6E, 1)
		return NoeTexture(name, width, height, rgba, noesis.NOESISTEX_RGBA32)


class TmntLevel:
	def __init__(self, index, bs):
		self.index = index
		scrollInfo0 = (bs.readUInt(), bs.readUShort(), -bs.readUByte(), bs.readUByte())
		scrollInfo1 = (bs.readUInt(), bs.readUShort(), -bs.readUByte(), bs.readUByte())		
		tileRefsAddr0 = bs.readUInt()
		tilesAddr0 = bs.readUInt()
		tileRefsAddr1 = bs.readUInt()
		tilesAddr1 = bs.readUInt()
		widthInfo0 = bs.readUShort()
		widthInfo1 = bs.readUShort()
		#the array at $1E2DA refers to custom map update routines for each level, which is what determines the type of data for each map.
		perMapFlags = (
			(0, 0),
			(0, 0),
			(1, 1),
			(0, 0),
			(0, 0),
			(0, 0),
			(0, 0),
			(0, 1),
			(0, 0),
			(0, 0)
		)
		flags0, flags1 = perMapFlags[index]
		self.maps = [TmntMap(scrollInfo0, tileRefsAddr0, tilesAddr0, widthInfo0, 0x800, flags0)]
		if tileRefsAddr0 != tileRefsAddr1 or tilesAddr0 != tilesAddr1:
			self.maps.append(TmntMap(scrollInfo1, tileRefsAddr1, tilesAddr1, widthInfo1, 0x800, flags1))
			
	def loadPalette(self, palRgba, bs):
		bs.seek(0x9F56 + self.index * 4, NOESEEK_ABS)
		palSetAddr = bs.readUInt()
		bs.seek(palSetAddr, NOESEEK_ABS)
		addrs = [bs.readUInt() for _ in range(4)]
		tmntLoadPalettes(bs, palRgba, 0, addrs[0], 8)
		tmntLoadPalettes(bs, palRgba, 0x200, addrs[1], 8)
		tmntLoadPalettes(bs, palRgba, 0x400, addrs[3], 16)
		tmntLoadPalettes(bs, palRgba, 0x800, addrs[2], 8)
		bs.seek(0x676E + self.index * 2, NOESEEK_ABS)
		self.reg6B = bs.readUByte()
		self.reg6E = bs.readUByte()


def tmntLoadLevels(codeData, tileData, texList):
	bs = NoeBitStream(codeData, NOE_BIGENDIAN)
	bs.seek(0x1E5A0, NOESEEK_ABS)
	levels = [TmntLevel(levelIndex, bs) for levelIndex in range(TMNT_LEVEL_COUNT)]
	palRgba = bytearray(0x1000)
	for level in levels:
		level.loadPalette(palRgba, bs)
		for mapIndex in range(len(level.maps)):
			map = level.maps[mapIndex]
			map.loadMap(bs)
			mapName = "tmnt_level%02i_map%02i"%(level.index, mapIndex)
			texList.append(map.drawTiles(tileData, palRgba, level.reg6B, level.reg6E, mapName, bs))


def tmntLoadRGBA(data, texList):
	imageBasePath = rapi.getDirForFilePath(rapi.getLastCheckedName())

	codeSets = (
		(128 * 1024, ("963-x23.j17", "963-x24.k17")),
		(64 * 1024, ("963-x21.j15", "963-x22.k15")),
	)
	tileSets = (
		(512 * 1024, ("963a28.h27", "963a29.k27")),
	)
	sprSets = (
		(512 * 1024, ("963a17.h4", "963a15.k4")),
		(512 * 1024, ("963a18.h6", "963a16.k6")),
	)
	
	codeData = tmntReadImageSets(imageBasePath, codeSets, 1)
	tileData = tmntTransformTileBits(tmntReadImageSets(imageBasePath, tileSets, 2))
	sprData = tmntTransformTileBits(tmntReadImageSets(imageBasePath, sprSets, 2))

	promData = readRomImages(imageBasePath, ("963a30.g7",), 0x100, ReadRomImageFlag_None) + readRomImages(imageBasePath, ("963a31.g19",), 0x100, ReadRomImageFlag_None)
	sprData = rapi.callExtensionMethod("tmnt_sprite_decode", sprData, promData)
	
	tileData = tmntInterleaveImagePlanes(tileData)
	sprData = tmntCreateSpritePages(tmntInterleaveImagePlanes(sprData), False)

	if LOAD_RAW:
		sprWidth = SPR_MACRO_WIDTH
		sprHeight = len(sprData) // (sprWidth >> 1)
		sprData = rapi.imageCopyChannelRGBA32(rapi.imageCopyChannelRGBA32(rapi.imageDecodeRaw(sprData, sprWidth, sprHeight, "r4"), 0, 1), 0, 2)
		texList.append(NoeTexture("tmnt_spr", sprWidth, sprHeight, sprData, noesis.NOESISTEX_RGBA32))
		
		#page up the tiles just for previewing purposes, otherwise we end up with a height beyond the capability of a lot of export formats
		tileWidth = sprWidth
		tileHeight = len(tileData) // (tileWidth >> 1)
		tileData = tmntCreateSpritePages(tileData, False)
		tileData = rapi.imageCopyChannelRGBA32(rapi.imageCopyChannelRGBA32(rapi.imageDecodeRaw(tileData, tileWidth, tileHeight, "r4"), 0, 1), 0, 2)
		texList.append(NoeTexture("tmnt_tile", tileWidth, tileHeight, tileData, noesis.NOESISTEX_RGBA32))

	if LOAD_LEVELS:
		tmntLoadLevels(codeData, tileData, texList)

	if LOAD_SPRITES:
		tmntLoadSprites(codeData, sprData, texList)

	rapi.processCommands("-texnorepfn")
	return 1


class Tmnt2FramePart(TmntFramePart):
	def __init__(self, bs):
		tileInfo = bs.readUShort()
		self.attrs = bs.readUShort()
		#put x/y-flip in same bits as K051960
		self.flags = ((self.attrs & 0x4000) >> 7) | ((self.attrs & 0x8000) >> 9)
		self.x = bs.readShort()
		self.y = -bs.readShort()
		xSize = (self.attrs >> 10) & 3
		ySize = (self.attrs >> 12) & 3
		self.width = (SPR_WIDTH << xSize)
		self.height = (SPR_HEIGHT << ySize)
		#coords are from center
		self.x -= (self.width >> 1)
		self.y -= (self.height >> 1)
		self.sprIndex = tileInfo
		self.hasShadow = (self.attrs & 0x80) != 0
		self.palOffset = (16 + (self.attrs & 0x1F)) << 6 #in rgba32 palette space
		self.mirrorFlags = (self.attrs >> 8) & 3
		pageOffsets = noesis.transformBits(self.sprIndex, bytearray((0, 2, 4, 1, 3, 5)))
		self.pageX = (pageOffsets & 7) * SPR_WIDTH
		self.pageY = (self.sprIndex >> 6) * SPR_MACRO_HEIGHT + (pageOffsets >> 3) * SPR_HEIGHT


class Tmnt2Frame(TmntFrame):
	def loadParts(self, bs, partCount):
		self.parts = [Tmnt2FramePart(bs) for _ in range(partCount)]


class Tmnt2FrameSet(TmntFrameSet):
	def loadFrames(self, bs, namePrefix):
		nextOffset = bs.tell()
		while not bs.checkEOF():
			bs.seek(nextOffset, NOESEEK_ABS)
			animCmdAndTime = bs.readUByte()
			pcOrTerminator = bs.readUByte()
			if len(self.frames) > 0 and animCmdAndTime == 0:
				break
			partCount = (pcOrTerminator & 0x7F) + 1
			partsOffset = bs.readUInt()
			if partsOffset >= bs.getSize():
				break
			dmgVel = bs.readShort()
			if dmgVel >= 0:
				#same as the first game, see $30E20
				bs.seek(8, NOESEEK_REL)
			nextOffset = bs.tell()
			bs.seek(partsOffset, NOESEEK_ABS)
			frame = Tmnt2Frame(bs, partCount)
			frame.name = namePrefix + "_set%06X_frame%02i"%(self.offset, len(self.frames))
			self.frames.append(frame)


def tmnt2LoadSprites(codeData, sprData, texList):
	bs = NoeBitStream(codeData, NOE_BIGENDIAN)

	defaultPalListAddrs = (0xB26A, 0xB2AA) #for second list, krang=0xB4AA, shredder=0xB52A - see lists at $0A74C
	defaultPalCount = 16
	palRgba = bytearray(0x1000)
	palOffset = 0x400
	for defaultPalListAddr in defaultPalListAddrs:
		tmntLoadPalettes(bs, palRgba, palOffset, defaultPalListAddr, defaultPalCount)
		palOffset += defaultPalCount * 16 * 4
		
	frameSets = []
	tmntFindFramesFromMoveList(bs, 0x1CF74, frameSets, "leo", Tmnt2FrameSet)
	tmntFindFramesFromMoveList(bs, 0x1ED70, frameSets, "mike", Tmnt2FrameSet)
	tmntFindFramesFromMoveList(bs, 0x209C2, frameSets, "don", Tmnt2FrameSet)
	tmntFindFramesFromMoveList(bs, 0x22550, frameSets, "raph", Tmnt2FrameSet)
	tmntFindFramesFromEnemyList(bs, 0x48E34, frameSets, Tmnt2FrameSet)
	#possible todo - suss out more frame addresses
	
	tmntRenderFrameSets(bs, sprData, frameSets, palRgba, texList)


class Tmnt2Map(TmntMap):
	def __init__(self, levelIndex, levelMapIndex, regs, palSetAddrs, bs):
		self.levelIndex = levelIndex
		self.levelMapIndex = levelMapIndex
		self.tileRefsAddr = bs.readInt()
		self.tilesAddr = bs.readInt()
		self.initTableIndex = bs.readUByte() #used by init function
		self.initFunctionIndex = bs.readUByte() #$32AC0 and $32A80
		self.tud0 = bs.readInt()
		self.tud1 = bs.readInt()
		#for intro scene:
		#reg6B = 0xE0 #$575C
		#reg6E = 0x0D #$576C
		#see $5F22
		self.reg6B = regs[5]
		self.reg6E = regs[6]
		self.palSetAddrs = palSetAddrs
		bs.seek(self.tileRefsAddr, NOESEEK_ABS)
		exCount = bs.readUShort()
		width = bs.readUShort()
		self.widthInBlocks = width >> 1
		self.heightInBlocks = 8
		self.tileRefsAddr = bs.tell() + exCount * width #from here, data is structured like the first game
		self.palBase = 0x1000 if levelMapIndex == 0 else 0xC00
		self.decodeFlags = 2
		self.layerIndex = 1 + self.levelMapIndex


def tmnt2LoadLevels(codeData, tileData, texList):
	bs = NoeBitStream(codeData, NOE_BIGENDIAN)
	levelIndices = []
	bs.seek(0x5642, NOESEEK_ABS)
	for levelIndex in range(TMNT2_LEVEL_COUNT):
		levelIndices.append((levelIndex, bs.readUByte(), bs.readUByte()))

	palRgba = bytearray(0x2000)

	bs.seek(0x5354, NOESEEK_ABS)
	palDestAddrs = [bs.readInt() for _ in range(8)]

	maps = []
	for levelIndex, uIndex, dataIndex in levelIndices:
		bs.seek(0xA74C + (dataIndex << 2), NOESEEK_ABS)
		levelPalAddrs = bs.readInt()		
		bs.seek(levelPalAddrs, NOESEEK_ABS)
		palSetAddrs = [bs.readInt() for _ in range(8)]
			
		bs.seek(0x63FC + (dataIndex << 3), NOESEEK_ABS)
		regs = bs.readBytes(8)
		
		bs.seek(0x46C56 + levelIndex * 0x12, NOESEEK_ABS)
		maps.append(Tmnt2Map(levelIndex, 0, regs, palSetAddrs, bs))
		bs.seek(0x46BA2 + levelIndex * 0x12, NOESEEK_ABS)
		maps.append(Tmnt2Map(levelIndex, 1, regs, palSetAddrs, bs))
		
	for map in maps:
		map.loadMap(bs)
		mapName = "tmnt_level%02i_map%02i"%(map.levelIndex, map.levelMapIndex)
		for palIndex in range(8):
			tmntLoadPalettes(bs, palRgba, (palDestAddrs[palIndex] & 0xFFFF) << 1, map.palSetAddrs[palIndex], 8 if palIndex <= 2 else 16)
		texList.append(map.drawTiles(tileData, palRgba, map.reg6B, map.reg6E, mapName, bs))


def tmnt2LoadRGBA(data, texList):
	imageBasePath = rapi.getDirForFilePath(rapi.getLastCheckedName())

	codeSets = (
		(128 * 1024, ("063uaa02.8e", "063uaa03.8g")),
		(128 * 1024, ("063uaa04.10e", "063uaa05.10g")),
	)
	tileSets = (
		(512 * 1024, ("063b12.16k", "063b11.12k")),
	)
	sprSets = (
		(1024 * 1024, ("063b09.7l", "063b07.3l")),
		(512 * 1024, ("063b10.7k", "063b08.3k")),
	)
	
	codeData = tmntReadImageSets(imageBasePath, codeSets, 1)
	tileData = tmntReadImageSets(imageBasePath, tileSets, 2)
	sprData = tmntReadImageSets(imageBasePath, sprSets, 2)

	tileData = tmntInterleaveImagePlanes(tileData)
	sprData = tmntCreateSpritePages(tmntInterleaveImagePlanes(sprData), True)

	if LOAD_RAW:
		sprWidth = SPR_MACRO_WIDTH
		sprHeight = len(sprData) // (sprWidth >> 1)
		sprData = rapi.imageCopyChannelRGBA32(rapi.imageCopyChannelRGBA32(rapi.imageDecodeRaw(sprData, sprWidth, sprHeight, "r4"), 0, 1), 0, 2)
		texList.append(NoeTexture("tmnt2_spr", sprWidth, sprHeight, sprData, noesis.NOESISTEX_RGBA32))
		
		tileWidth = sprWidth
		tileHeight = len(tileData) // (tileWidth >> 1)
		tileData = tmntCreateSpritePages(tileData, False)
		tileData = rapi.imageCopyChannelRGBA32(rapi.imageCopyChannelRGBA32(rapi.imageDecodeRaw(tileData, tileWidth, tileHeight, "r4"), 0, 1), 0, 2)
		texList.append(NoeTexture("tmnt2_tile", tileWidth, tileHeight, tileData, noesis.NOESISTEX_RGBA32))

	if LOAD_LEVELS:
		tmnt2LoadLevels(codeData, tileData, texList)

	if LOAD_SPRITES:
		tmnt2LoadSprites(codeData, sprData, texList)

	rapi.processCommands("-texnorepfn")
	return 1
