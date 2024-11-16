from inc_noesis import *
import os

SNES8_PALETTE_VALUE = 2
SNES8_DEFAULT_PRIORITY = 0

SNES4_DEFAULT_PRIORITY = 0

def registerNoesisTypes():
	handle = noesis.registerTool("SNES-8 Chop", lambda u: tileChopRunToolGeneric(snes8ToolMethod), "Chop into 8-bit SNES tiles.")
	noesis.setToolSubMenuName(handle, "SNES")	
	noesis.setToolFlags(handle, noesis.NTOOLFLAG_CONTEXTITEM)
	noesis.setToolVisibleCallback(handle, tileChopContextVisible)
	
	handle = noesis.registerTool("SNES-4 Chop", lambda u: tileChopRunToolGeneric(snes4ToolMethod), "Chop into 4-bit SNES tiles.")
	noesis.setToolSubMenuName(handle, "SNES")	
	noesis.setToolFlags(handle, noesis.NTOOLFLAG_CONTEXTITEM)
	noesis.setToolVisibleCallback(handle, tileChopContextVisible)	
	return 1

def tileChopContextVisible(toolIndex, selectedFile):
	if selectedFile is None or (noesis.getFormatExtensionFlags(os.path.splitext(selectedFile)[1]) & noesis.NFORMATFLAG_IMGREAD) == 0:
		return 0
	return 1
		
def tileChopRunToolGeneric(toolMethod):
	srcName = noesis.getSelectedFile()
	if not srcName or not os.path.exists(srcName):
		return 0

	noesis.logPopup()
		
	noeMod = noesis.instantiateModule()
	noesis.setModuleRAPI(noeMod)

	with open(srcName, "rb") as f:
		data = f.read()
		tex = rapi.loadTexByHandler(data, srcName)
		if not tex or not noeSafeGet(tex, "palColorData"):
			noesis.logPopup()
			print("File must be a valid, palettized image.")
			r = -1
		else:
			r = toolMethod(srcName, tex)
	
	noesis.freeModule(noeMod)

	return r
		
def snes8ToolMethod(srcName, tex):
	tileList, tileData = rapi.callExtensionMethod("chop_8x8_tiles", tex.palIndexData, tex.width, tex.height, 0)
	if not tileList or not tileData:
		return -1
	
	tileList = noeUnpack("<" + "I" * (len(tileList) // 4), tileList)
	chrCount = len(tileData) // 64
	if chrCount > 1023:
		print("Too many unique tiles:", chrCount)
		return -1
		
	tileFile = srcName + ".mp1"
	chrFile = srcName + ".ft8"
	with open(tileFile, "wb") as fw:
		for tile in tileList:
			snesTile = tile & 1023
			if tile & noesis.TILE_CHOP_FLAG_MIRROR_X:
				snesTile |= 16384
			if tile & noesis.TILE_CHOP_FLAG_MIRROR_Y:
				snesTile |= 32768
			snesTile |= (SNES8_PALETTE_VALUE << 10)
			snesTile |= (SNES8_DEFAULT_PRIORITY << 13)
			fw.write(noePack("<H", snesTile))
	print("Wrote", tileFile)
			
	with open(chrFile, "wb") as fw:
		fw.write(rapi.callExtensionMethod("snes_encodechr_m4b0", tileData))
	print("Wrote", chrFile)
	
	return 0

def snes4ToolMethod(srcName, tex):
	if (tex.width & 15) or (tex.height & 15):
		print("MP2 files must be block-aligned.")
		return -1

	tileList, tileData = rapi.callExtensionMethod("chop_8x8_tiles", tex.palIndexData, tex.width, tex.height, 0)
	if not tileList or not tileData:
		return -1
	
	tileData = bytearray(tileData) #we'll be modifying it to map into 4-bit palette indices
	tileList = noeUnpack("<" + "I" * (len(tileList) // 4), tileList)
	chrCount = len(tileData) // 64
	if chrCount > 1023:
		print("Too many unique tiles:", chrCount)
		return -1
		
	#just assign a palette to each chr
	chrPals = []
	for chrIndex in range(chrCount):
		chrOffset = chrIndex * 64
		minPalIndex = 256
		for offset in range(64):
			c = tileData[chrOffset + offset]
			minPalIndex = min(minPalIndex, c)
		minPalIndex &= ~15
		if minPalIndex > (7 * 16):
			print("Warning: Palette out of range for chr", chrIndex)
		#map the indices into the range for the selected palette bank
		maxPixelIndex = 0
		for offset in range(64):
			pixelOffset = chrOffset + offset
			tileData[pixelOffset] -= minPalIndex
			maxPixelIndex = max(maxPixelIndex, tileData[pixelOffset])
		if maxPixelIndex >= 16:
			print("Warning: Pixel value", maxPixelIndex, "goes out of 4-bit range for chr", chrIndex)
		chrPals.append(minPalIndex // 16)
		
	cnvFile = srcName + ".cv2"
	mapFile = srcName + ".mp2"
	chrFile = srcName + ".era"
	uniqueBlockMap = {}
	uniqueBlockCount = 0
	with open(cnvFile, "wb") as fCnv, open(mapFile, "wb") as fMap:
		tileOffsets = (
			(0, 0),
			(1, 0),
			(0, 1),
			(1, 1)
		)
		widthInTiles = tex.width // 8
		heightInTiles = tex.height // 8
		for y in range(0, heightInTiles, 2):
			for x in range(0, widthInTiles, 2):
				blockTiles = []
				for xOffset, yOffset in tileOffsets:
					tileX = x + xOffset
					tileY = y + yOffset
					tile = tileList[tileY * widthInTiles + tileX]

					chrIndex = tile & 1023
					snesTile = chrIndex
					if tile & noesis.TILE_CHOP_FLAG_MIRROR_X:
						snesTile |= 16384
					if tile & noesis.TILE_CHOP_FLAG_MIRROR_Y:
						snesTile |= 32768
					snesTile |= (chrPals[chrIndex] << 10)
					snesTile |= (SNES4_DEFAULT_PRIORITY << 13)
					blockTiles.append(snesTile)
				#see if we already have this particular block of tiles mapped.
				#if not, write the tiles to the cnv before moving on.
				blockTiles = tuple(blockTiles)
				if blockTiles not in uniqueBlockMap:
					uniqueBlockMap[blockTiles] = uniqueBlockCount
					uniqueBlockCount += 1
					for blockTile in blockTiles:
						fCnv.write(noePack("<H", blockTile))
				fMap.write(noePack("<H", uniqueBlockMap[blockTiles]))
	print("Wrote", mapFile)
	print("Wrote", cnvFile)

	with open(chrFile, "wb") as fw:
		fw.write(rapi.callExtensionMethod("snes_encodechr_m1b0", tileData))
	print("Wrote", chrFile)
	
	return 0
