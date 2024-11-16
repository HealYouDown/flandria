from inc_noesis import *
import os

"""
LICENSE:
This script is provided for reference and research purposes only.

This script may not be used in any way for the development of a Blender importer. Be aware that open source software is used very insidiously in today's culture of capitalist exploitation.
Instead of cannibalizing functionality for Blender so that Microsoft, Facebook, and Activision can laugh at you from on high (in between large gulps of cheap artist/engineer labor), consider
helping Noesis! There are good reasons that Noesis isn't open-sourced in this capitalist hellscape, but it is free software in the truest sense. Its aim is to provide knowledge and insight,
which is why it's named Noesis. To that end, you can help too. Maybe try stopping by the XeNTaX Discord to share in the knowledge. Chances are, if you're considering using your time to rip
functionality out of Noesis instead of doing some real reverse engineering, the community has a lot it can teach you.

(c) 2021 Rich Whitehouse
"""

#SBI_ID_* maps to offset+size pairs at the start of SYSTEM.BIN.
#MIF_TMP_ID_* maps to offset+size pairs at the start of MAPINFO1.BIN.
#MIF_ID_* maps to offset+size pairs at the start of MAPINFO2.BIN.
SBI_ID_ITEMLIST = 1
SBI_ID_SHOPITEM = 2
SBI_ID_TEX_CLEAR_TEX = 10
SBI_ID_TEX_SHOP_TEX = 11
SBI_ID_TEX_SHOP_CLUT = 12
SBI_ID_TEX_HINT_TEX = 13
SBI_ID_TEX_HINT_CLUT = 14
SBI_ID_TEX_WHOUSE_TEX = 15
SBI_ID_TEX_WHOUSE_CLUT = 16
SBI_ID_TEX_GAMEOVER_TEX = 17
SBI_ID_TEX_GAMEOVER_CLUT = 18
SBI_ID_TEX_SAVEWIN_TEX = 19
SBI_ID_TEX_SAVEWIN_CLUT = 20
SBI_ID_TEX_MEZAWIN_TEX = 21
SBI_ID_TEX_MEZAWIN_CLUT = 22
SBI_ID_COUNT = 23
MIF_TMP_ID_AANIMSEQ = 0
MIF_TMP_ID_ZANIMSEQ = 1
MIF_TMP_ID_MLIST1 = 3
MIF_TMP_ID_MLIST2 = 4
MIF_TMP_ID_ZONEMDL = 5
MIF_TMP_ID_RANIMSEQ = 6
MIF_TMP_ID_ITEMLIST = 7
MIF_TMP_ID_ITEM_MODEL = 8
MIF_TMP_ID_TEX_LS_TEX = 9
MIF_TMP_ID_TEX_LS_CLUT = 10
MIF_TMP_ID_TEX_ANIM0_TEX = 11
MIF_TMP_ID_TEX_ANIM0_CLUT = 12
MIF_TMP_ID_TEX_ANIM1_TEX = 13
MIF_TMP_ID_TEX_ANIM1_CLUT = 14
MIF_TMP_ID_TEX_ANIM2_TEX = 15
MIF_TMP_ID_TEX_ANIM2_CLUT = 16
MIF_TMP_ID_TEX_ANIM3_TEX = 17
MIF_TMP_ID_TEX_ANIM3_CLUT = 18
MIF_TMP_ID_TEX_ANIM4_TEX = 19
MIF_TMP_ID_TEX_ANIM4_CLUT = 20
MIF_TMP_ID_TEX_ANIM5_TEX = 21
MIF_TMP_ID_TEX_ANIM5_CLUT = 22
MIF_TMP_ID_TEX_ANIM6_TEX = 23
MIF_TMP_ID_TEX_ANIM6_CLUT = 24
MIF_TMP_ID_TEX_ANIM7_TEX = 25
MIF_TMP_ID_TEX_ANIM7_CLUT = 26
MIF_TMP_ID_TEX_ENV = 27
MIF_TMP_ID_COUNT = 28
MIF_ID_ROLIST = 0
MIF_ID_TALIST = 1
MIF_ID_ACHR_MDL = 8
MIF_ID_SOBJ_MDL = 9
MIF_ID_COUNT = 10

#you may find my naming and conventions odd in here. it's inspired by original structure/data/etc. names wherever possible.
#however, being originally written by japanese developers with varying degrees of english writing ability, some the naming is a little questionable.
MAX_ZONE_MODEL = 30
MAX_SCHR_ID_MODEL = 1
MAX_RCHR_ID_MODEL = 251
MAX_ACHR_ID_MODEL = 32
MAX_DCHR_ID_MODEL = 64
MAX_ZCHR_ID_MODEL = 100
SCHR_ID_TAIL = MAX_SCHR_ID_MODEL
RCHR_ID_TAIL = SCHR_ID_TAIL + MAX_RCHR_ID_MODEL
ACHR_ID_TAIL = RCHR_ID_TAIL + MAX_ACHR_ID_MODEL
DCHR_ID_TAIL = ACHR_ID_TAIL + MAX_DCHR_ID_MODEL
ZCHR_ID_TAIL = DCHR_ID_TAIL + MAX_ZCHR_ID_MODEL
SCHR_ID_BASE = 0
RCHR_ID_BASE = SCHR_ID_TAIL
ACHR_ID_BASE = RCHR_ID_TAIL
DCHR_ID_BASE = ACHR_ID_TAIL
ZCHR_ID_BASE = DCHR_ID_TAIL

GS_PSMCT32 = 0
GS_PSMCT16 = 2
GS_PSMT8 = 19
GS_PSMT4 = 20

TEX_MAP_FLAG = 0x1000
TEX_MAP_MASK = ~TEX_MAP_FLAG

#the game uses a terrible hack in many locations which breaks/resets/skips when the name is "1cell.bin"
END_MARKER = "1cell.bin"

#custom extension tacked onto models for easy identification
MODEL_EXT = ".chulip_mdl"

#determines the framerate for the noesis keyframe evaluator
CHULIP_ANIM_EVAL_FRAMERATE = 30.0

#determines the playback framerate in noesis preview
CHULIP_ANIM_PLAYBACK_FRAMERATE = 60.0

#if True, sets materials up for PBR rendering
USE_PBR_MATERIALS = True

#if True, attempts to load shared textures when possible
ALLOW_SHARED_TEXTURE_LOAD = True

#if True, when loading shared textures, loads all subsequent textures in a "stack" and sets the material to animate through them
LOAD_ALL_ANIM_TEXTURES = False

#custom header used to dump detail header along with standard model binary
DETAIL_HEADER_ID = 0xC001D00D
DETAIL_HEADER_VERSION = 1
WRITE_DETAIL_HEADER = True

#this is a common ps2 tactic, where some textures are pre-arranged to be transferred to gs memory as PSMCT32 in order to speed up the upload.
#in this case, the developer chose a very specific set of criteria.
TWIDDLE_MAPPING_4 = (
	(64, 128, 64, 16),
	(128, 64, 32, 64),
	(128, 128, 64, 32),
	(128, 256, 64, 64),
	(256, 32, 32, 32),
	(256, 128, 128, 32),
	(256, 256, 128, 64)
)
TWIDDLE_MAPPING_8 = (
	(256, 64, 128, 32),
	(256, 128, 128, 64),
	(256, 256, 128, 128)
)


def registerNoesisTypes():
	handle = noesis.register("Chulip Archive", ".bin")
	noesis.setHandlerExtractArc(handle, mapInfoExtract)

	handle = noesis.register("Chulip Model", MODEL_EXT)
	noesis.setHandlerTypeCheck(handle, checkChulipModel)
	noesis.setHandlerLoadModel(handle, loadChulipModel)
	
	return 1


class ModelDetail:
	DataSize = 64
	def __init__(self, bs, modelIndex, baseOffset, setIndex):
		self.modelIndex = modelIndex
		self.name = noeStrFromBytes(bs.readBytes(32).split(b"\0")[0])
		self.texShare = bs.readUByte()
		self.texShareInfo = [ModelTexShareInfo(bs) for _ in range(8)]
		self.width = bs.readUByte()
		self.sendTex = bs.readUByte()
		bs.readUByte() #pad
		self.size = bs.readUInt()
		self.offset = bs.readUInt()
		self.baseOffset = baseOffset
		self.setIndex = setIndex
		bs.readUInt() #pad


class AnimDetail:
	def __init__(self, bs, endOffset):
		self.sequences = []
		#see readAnimList
		while bs.tell() < endOffset:
			startFrame = bs.readUShort()
			endFrame = bs.readUShort()
			if startFrame == 0xFFFF:
				break
			self.sequences.append((startFrame, endFrame))


class ZoneModel:
	def __init__(self, bs, zoneIndex):
		self.size = bs.readUInt()
		self.offset = bs.readUInt()
		self.id = bs.readUInt()


class ZoneModels:
	def __init__(self, bs, zoneIndex):
		modelCount = bs.readUInt()
		bs.readUInt() #size
		bs.readUInt() #offset
		self.zoneModels = [ZoneModel(bs, zoneIndex) for _ in range(modelCount)]


class RoomModel:
	def __init__(self, bs):
		self.size = bs.readUInt()
		self.offset = bs.readUInt()
		self.id = bs.readUInt()
		self.loadId = bs.readUInt()
		self.trn = [bs.readFloat() for _ in range(3)]
		self.rot = bs.readFloat()


class RoomModels:
	def __init__(self, bs):
		modelCount = bs.readUInt()
		bs.readUInt() #size
		bs.readUInt() #offset
		self.roomModels = [RoomModel(bs) for _ in range(32)]
		#although we have the count here, the max (32) is still being loaded from disc (and there's often garbage data in the unused entries)
		self.roomModels = self.roomModels[:modelCount]


class ModelTexShareInfo:
	def __init__(self, bs):
		self.texAnimManId = bs.readUByte()
		self.texDstId = bs.readUByte()


class FWDataHeader:
	def __init__(self, bs):
		self.offset = bs.tell()
		#offsets for some types are not in order, and extra data is occasionally placed beyond the last offset, making this stuff a real pain to parse over without knowing an offset/size.
		dataOffsets = [bs.readUInt() for _ in range(15)]
		#print("Data header:", dataOffsets)
		self.shapeOffset = dataOffsets[0]
		self.baseMatrixOffset = dataOffsets[1]
		self.texOffset = dataOffsets[2]
		self.hieOffset = dataOffsets[3]
		self.shapeMfOffset = dataOffsets[4]
		self.animOffset = dataOffsets[5]
		self.animKfOffset = dataOffsets[6]
		self.animKvOffset = dataOffsets[7]
		
		self.shareInfoOffset = dataOffsets[8]
		self.shareVDataOffset = dataOffsets[9]
		self.shareNDataOffset = dataOffsets[10]
		self.shareVIndexOffset = dataOffsets[11]
		self.shareNIndexOffset = dataOffsets[12]
		self.shareVOffset = dataOffsets[13]
		self.shareNOffset = dataOffsets[14]


class FWShapeData:
	def __init__(self, bs):
		bs.seek(12, NOESEEK_REL)
		shapeCount = bs.readUInt()
		self.shapeOffsets = []
		for _ in range(shapeCount):
			shapeOffset = bs.tell()
			bs.seek(4, NOESEEK_REL)
			shapeSizeInDwords = bs.readUInt()
			bs.seek(shapeOffset + (shapeSizeInDwords + 4) * 4, NOESEEK_ABS)
			self.shapeOffsets.append(shapeOffset)
			

class FWShapeGeo:
	def __init__(self, bs):
		bs.readInt() #unused
		self.geoSize = bs.readInt()
		self.primFlags = bs.readInt() #low 3 bits are prim type; 3=trilist, 4=tristrip. 0x40=alpha blend. (see GS_PRIM)
		self.vertCount = bs.readInt()

		#fortunately for us, the vertex layout is always the same and already in unpacked form. this means we don't have to care about using micro_data and emulating VIF commands.
		self.posData = bytearray(bs.readBytes(self.vertCount * 16)) #may be modified for share verts
		self.nrmData = bytearray(bs.readBytes(self.vertCount * 16)) #may be modified for share verts
		self.uvwData = bs.readBytes(self.vertCount * 16)
		self.clrData = bytearray(bs.readBytes(self.vertCount * 16))
		
		if self.vertCount > 0:
			#convert range from 0..255 for color and 0..128 for alpha
			alphaScale = 255.0 / 128.0
			for vertIndex in range(self.vertCount):
				alphaOffset = (vertIndex << 4) + 12
				f = noeUnpack("<f", self.clrData[alphaOffset : alphaOffset + 4])[0]
				self.clrData[alphaOffset : alphaOffset + 4] = noePack("<f", f * alphaScale)
			self.clrData = rapi.scaleAndBiasPackedFloats(self.clrData, 1.0 / 255.0, 0.0, 0.0, 1.0)
		
		self.weightIndexData = bytearray(noePack("<%iI"%self.vertCount, *([0] * self.vertCount))) #may be modified for share verts
		self.weightValueData = noePack("<%if"%self.vertCount, *([1.0] * self.vertCount))


class FWShapeDraw:
	def __init__(self, bs):
		bs.readInt() #unused
		geoCount = bs.readInt()
		self.texIndex = bs.readInt()
		self.texIsPresent = bs.readInt()
		bs.seek(8 * 4, NOESEEK_REL) #runtime just skips right over all of this
		self.geos = [FWShapeGeo(bs) for _ in range(geoCount)]

	def renderToContext(self, texList, texIndexMap, mtlList, mtlSet):
		useTexture = self.texIsPresent != 0
		texSuffix = "_tex%02i"%self.texIndex if useTexture else "_notex"
		for geo in self.geos:
			if geo.vertCount > 0:
				useAlphaBlending = (geo.primFlags & 0x40) != 0
				absTexIndex = texIndexMap.get(self.texIndex, -1) if useTexture else -1
				tex = texList[absTexIndex] if absTexIndex >= 0 else None
				if tex and not tex.chuUsesClut:
					#even if the blend flag isn't set, we want to blend if we're using a full rgba32 texture.
					#this emulates the behavior of the alpha expanding bit only being effective when the texture doesn't contain an 8-bit alpha.
					useAlphaBlending = True
				blendSuffix = "_blended" if useAlphaBlending else ""
				mtlName = "chumat" + texSuffix + blendSuffix

				if mtlName not in mtlSet:
					#create the material on-demand
					mtlSet.add(mtlName)
					mtl = NoeMaterial(mtlName, "")
					if tex:
						mtl.setTexture(tex.name)
						if useAlphaBlending:
							mtl.setBlendMode("GL_SRC_ALPHA", "GL_ONE_MINUS_SRC_ALPHA")
							mtl.setAlphaTest(0.05)
						else:
							#match default behavior for GS_TEXA
							mtl.setDefaultBlend(0)
							mtl.setAlphaTest(0.5)
						texCount = noeSafeGet(tex, "chuTexCount")
						if texCount:
							cycleTime = 250.0 #250ms
							mtl.setExpr_texidx("%i + mod(time * %f, %i)"%(absTexIndex, 1.0 / cycleTime, texCount))
					if USE_PBR_MATERIALS:
						mtl.setEnvTexture(os.path.join(noesis.getScenesPath(), "sample_pbr_e3.dds"))
						mtl.flags |= noesis.NMATFLAG_PBR_METAL | noesis.NMATFLAG_PBR_SPEC_IR_RG
						mtl.flags2 |= noesis.NMATFLAG2_PREFERPPL | noesis.NMATFLAG2_ENV_FLIP_Y
						mtl.setMetal(0.0, 0.0)
						mtl.setRoughness(0.0, 0.7)
					mtlList.append(mtl)

				rapi.rpgSetMaterial(mtlName)

				rapi.rpgBindBoneIndexBuffer(geo.weightIndexData, noesis.RPGEODATA_INT, 4, 1)
				rapi.rpgBindBoneWeightBuffer(geo.weightValueData, noesis.RPGEODATA_FLOAT, 4, 1)
				rapi.rpgBindPositionBuffer(geo.posData, noesis.RPGEODATA_FLOAT, 16)
				rapi.rpgBindNormalBuffer(geo.nrmData, noesis.RPGEODATA_FLOAT, 16)
				rapi.rpgBindUV1Buffer(geo.uvwData, noesis.RPGEODATA_FLOAT, 16)
				rapi.rpgBindColorBuffer(geo.clrData, noesis.RPGEODATA_FLOAT, 16, 4)

				#for shapes, we have no explicit index data, so vertices are repeated to form triangles
				primType = noesis.RPGEO_TRIANGLE_STRIP if ((geo.primFlags & 7) == 4) else noesis.RPGEO_TRIANGLE
				rapi.rpgCommitTriangles(None, noesis.RPGEODATA_INT, geo.vertCount, primType, 1)

				rapi.rpgClearBufferBinds()
		

class FWShape:
	def __init__(self, bs):
		bs.readUInt() #unused
		self.size = bs.readUInt()
		bs.readUInt() #unused
		materialCount = bs.readUInt()
		self.vertCount = 0
		self.draws = [FWShapeDraw(bs) for _ in range(materialCount)]
		for draw in self.draws:
			for geo in draw.geos:
				geo.vertIndex = self.vertCount
				self.vertCount += geo.vertCount


class FWPerBoneShareInfo:
	def __init__(self, bs):
		self.posIndex = bs.readUInt()
		self.posCount = bs.readUInt()
		self.nrmIndex = bs.readUInt()
		self.nrmCount = bs.readUInt()


class FWShareInfoSection:
	def __init__(self, bs):
		self.srcVertIndex = bs.readInt()
		self.dstGeoIndex = bs.readInt()
		bs.readInt() #"geomID", unused by runtime, don't trust it
		self.vertCount = bs.readInt()		


class FWShareInfo:
	def __init__(self, bs):
		bs.seek(8, NOESEEK_REL)
		self.shareShapeIndex = bs.readUInt()
		shareCount = bs.readUInt()
		self.sections = [FWShareInfoSection(bs) for _ in range(shareCount)]
		
	def calculateIndexCount(self):
		maxCount = 0
		for section in self.sections:
			maxCount = max(maxCount, section.srcVertIndex + section.vertCount)
		return maxCount


class FWHierarchyBone:
	def __init__(self, bs):
		self.trn = [bs.readFloat() for _ in range(4)]
		self.rot = [bs.readFloat() for _ in range(4)]
		self.scl = [bs.readFloat() for _ in range(4)]
		bs.readInt() #may be shape reference, but not used by runtime, so don't trust it
		self.parentIndex = bs.readInt()
		self.childIndex = bs.readInt()
		self.siblingIndex = bs.readInt()
		self.localMat = transformFromChuTRS(self.trn, self.rot, self.scl)


class FWHierarchyMat:
	def __init__(self, bs):
		bs.readInt() #"rorder"
		bs.readInt() #reserved0
		bs.readInt() #reserved1
		self.shapeIndex = bs.readInt()
		self.localMat = NoeMat44(([bs.readFloat() for _ in range(4)], [bs.readFloat() for _ in range(4)], [bs.readFloat() for _ in range(4)], [bs.readFloat() for _ in range(4)])).transpose()
		self.lightMat = NoeMat44(([bs.readFloat() for _ in range(4)], [bs.readFloat() for _ in range(4)], [bs.readFloat() for _ in range(4)], [bs.readFloat() for _ in range(4)])).transpose()


class FWAnimBone:
	def __init__(self, bs):
		self.boneIndex = bs.readInt() #"hierarchy"
		self.keyCount = bs.readInt()
		self.kfIndex = bs.readInt()
		self.kvIndex = bs.readInt()


class FWAnimKeyTime:
	def __init__(self, bs):
		bs.seek(8, NOESEEK_REL)
		sizeInDwords = bs.readInt()
		bs.readInt() #unused
		#"time" here is the frame index, so not tied to any particular framerate
		self.times = [bs.readInt() for _ in range(sizeInDwords)]


class FWAnimKeyValue:
	def __init__(self, bs):
		bs.seek(8, NOESEEK_REL)
		sizeInDwords = bs.readInt()
		bs.readInt() #unused
		self.values = [bs.readFloat() for _ in range(sizeInDwords)]


class TexAnim:
	DataSize = 32
	def __init__(self, bs):
		self.texId = bs.readUShort()
		self.clutId = bs.readUShort()
		self.srcId = bs.readUShort()
		self.gsTex01 = bs.readUShort()
		self.tbp = bs.readUShort()
		self.cbp = bs.readUShort()
		self.width = bs.readUShort()
		self.height = bs.readUShort()
		self.texSize = bs.readUShort()
		self.clutSize = bs.readUShort()
		self.cur = bs.readUShort()
		self.pad = [bs.readUShort() for _ in range(5)]


def readRelativeFile(localPath, maxDepth = 1):
	currentPath = rapi.getDirForFilePath(rapi.getLastCheckedName())
	for currentDepth in range(maxDepth):
		#always start at one .., the path relationship between global index and global data remains the same as local index/data
		currentPath = os.path.join(currentPath, "..")
		fullPath = os.path.abspath(os.path.join(currentPath, localPath))
		if os.path.exists(fullPath):
			with open(fullPath, "rb") as f:
				return f.read()
	return None


def readSectionData(bs, sectionInfo):
	sectionOffset, sectionSize = sectionInfo
	bs.seek(sectionOffset, NOESEEK_ABS)
	return bs.readBytes(sectionSize)


def readModelDetails(bs, sectionInfo):
	sectionOffset, sectionSize = sectionInfo
	bs.seek(sectionOffset, NOESEEK_ABS)
	modelCount = sectionSize // ModelDetail.DataSize
	modelDetails = []
	baseOffset = 0
	setIndex = 0
	for modelIndex in range(modelCount):
		md = ModelDetail(bs, modelIndex, baseOffset, setIndex)
		if md.name == END_MARKER:
			if baseOffset != 0:
				setIndex += 1
			baseOffset = 0
		else:
			baseOffset += md.size
			modelDetails.append(md)
	return modelDetails
	
	
def readAnimDetails(bs, sectionInfo):
	sectionOffset, sectionSize = sectionInfo
	bs.seek(sectionOffset, NOESEEK_ABS)
	endOffset = sectionOffset + sectionSize
	animDetails = []
	while bs.tell() < endOffset:
		animDetails.append(AnimDetail(bs, endOffset))
	return animDetails


def calculateMaxZoneFromPath():
	#this is a hardcoded table in the executable (we only need to care about width and height for each entry)
	bzi = {
		"map00" : (6, 13),
		"map01" : (9, 9),
		"map02" : (8, 8),
		"map03" : (4, 4),
		"map04" : (8, 8),
		"map05" : (15, 5),
		"map06" : (10, 6),
		"map07" : (16, 2),
		"map97" : (4, 4),
		"map98" : (6, 13),
		"map99" : (4, 4)
	}
	mapPathPart = rapi.getLocalFileName(os.path.abspath(os.path.join(rapi.getDirForFilePath(rapi.getLastCheckedName()), ".."))).lower()
	if mapPathPart not in bzi:
		print("Error: Failed to determine map index from path:", rapi.getLastCheckedName(), "-", mapPathPart)
		return -1
	zoneWidth, zoneHeight = bzi[mapPathPart]
	return zoneWidth * zoneHeight


def writeDetailHeader(modelDetail, animDetail):
	if not WRITE_DETAIL_HEADER:
		return bytearray()
	bs = NoeBitStream()
	bs.writeUInt(DETAIL_HEADER_ID)
	bs.writeUInt(DETAIL_HEADER_VERSION)
	if modelDetail:
		bs.writeUInt(1)
		bs.writeUInt(modelDetail.modelIndex)
		bs.writeUInt(modelDetail.texShare)
		for texShareInfo in modelDetail.texShareInfo:
			bs.writeUByte(texShareInfo.texAnimManId)
			bs.writeUByte(texShareInfo.texDstId)
	else:
		bs.writeUInt(0)
	if animDetail:
		bs.writeUInt(1)
		bs.writeUInt(len(animDetail.sequences))
		for startFrame, endFrame in animDetail.sequences:
			bs.writeUInt(startFrame)
			bs.writeUInt(endFrame)
	else:
		bs.writeUInt(0)
	return bs.getBuffer()


def exportModelWithDetail(modelDetail, modelData, modelPrefix, animDetail = None):
	exportName = modelPrefix + (modelDetail.name.replace("..", "").replace("/", "_") if modelDetail else "") + MODEL_EXT
	print("Writing", exportName)
	rapi.exportArchiveFile(exportName, writeDetailHeader(modelDetail, animDetail) + modelData)


def exportModelDetailSet(modelDetails, modelData, setIndex, modelPrefix, animDetails = None):
	for modelDetail in modelDetails:
		if modelDetail.setIndex == setIndex or setIndex < 0:
			animDetail = animDetails[modelDetail.modelIndex] if animDetails and modelDetail.modelIndex < len(animDetails) else None
			exportModelWithDetail(modelDetail, modelData[modelDetail.baseOffset : modelDetail.baseOffset + modelDetail.size], modelPrefix, animDetail)


def info1Handler(bs, sectionInfos):	
	mi2Data = readRelativeFile(r"DAT\MAPINFO2.BIN")
	scmdlData = readRelativeFile(r"MDL\SCMDL.PAK")
	zoneDatas = []
	while True:
		zoneData = readRelativeFile(r"MDL\ZONEMDL%i.PAK"%len(zoneDatas))
		if not zoneData:
			break
		zoneDatas.append(zoneData)
	
	if not mi2Data:
		print("Failed to load MAPINFO2 data.")
		return 0
	if not scmdlData:
		print("Failed to load SCMDL data.")
		return 0
	if len(zoneDatas) == 0:
		print("Failed to any ZONEMDL data.")
		return 0
	
	model1Details = readModelDetails(bs, sectionInfos[MIF_TMP_ID_MLIST1])
	model2Details = readModelDetails(bs, sectionInfos[MIF_TMP_ID_MLIST2])
	modelItemDetails = readModelDetails(bs, sectionInfos[MIF_TMP_ID_ITEMLIST])
	
	aAnimDetails = readAnimDetails(bs, sectionInfos[MIF_TMP_ID_AANIMSEQ])
	zAnimDetails = readAnimDetails(bs, sectionInfos[MIF_TMP_ID_ZANIMSEQ])

	print("Extracting zone models.")
	zoneBs = NoeBitStream(readSectionData(bs, sectionInfos[MIF_TMP_ID_ZONEMDL]))
	zoneModelCount = 0
	zoneDataIndex = 0
	previousOffset = 0
	#the correct way to know how many ZoneModels we need to read is to reference the hardcoded table.
	#this is pretty gross and requires us to map the bin path back to a zone index.
	#unfortunately, we have to do this to avoid a lot of garbage-data-check cases, because there's often a significant amount of garbage data placed on the tail of MIF_TMP_ID_ZONEMDL.
	maxZone = calculateMaxZoneFromPath()
	if maxZone >= 0:
		for zoneIndex in range(maxZone):
			zone = ZoneModels(zoneBs, zoneIndex)
			for zoneModel in zone.zoneModels:
				#this is a slight hack to avoid having to map model id's
				if zoneModel.offset < previousOffset:
					zoneDataIndex += 1
				previousOffset = zoneModel.offset
				if zoneDataIndex < len(zoneDatas):
					zoneData = zoneDatas[zoneDataIndex]
					modelData = zoneData[zoneModel.offset : zoneModel.offset + zoneModel.size]
					modelDetail = model2Details[zoneModel.id - ZCHR_ID_BASE] if zoneModel.id >= ZCHR_ID_BASE and zoneModel.id < ZCHR_ID_TAIL else None
					animDetail = zAnimDetails[zoneModel.id - ZCHR_ID_BASE] if modelDetail else None
					exportModelWithDetail(modelDetail, modelData, "zone_" if modelDetail else "zone_model_%04i"%zoneModelCount, animDetail)
				else:
					print("Error: Zone models out of range for loaded data:", zoneDataIndex)
				zoneModelCount += 1

	mi2Bs = NoeBitStream(mi2Data)
	mi2Bs.seek(4, NOESEEK_ABS)
	mi2SectionCount = (mi2Bs.readUInt() - 8) // 8
	mi2SectionInfos = [(mi2Bs.readUInt(), mi2Bs.readUInt()) for _ in range(mi2SectionCount)]

	achrData = readSectionData(mi2Bs, mi2SectionInfos[MIF_ID_ACHR_MDL])
	sobjData = readSectionData(mi2Bs, mi2SectionInfos[MIF_ID_SOBJ_MDL])
	itemData = readSectionData(bs, sectionInfos[MIF_TMP_ID_ITEM_MODEL])

	print("Extracting achr models.")
	exportModelDetailSet(model1Details, achrData, 1, "achr_", aAnimDetails)

	print("Extracting sobj models.")
	exportModelDetailSet(model2Details, sobjData, 2, "sobj_")

	print("Extracting item models.")
	exportModelDetailSet(modelItemDetails, itemData, -1, "item_")

	#special case, this entry always covers the model in scmdl
	print("Extracting scmdl models.")
	scmdlDetail = model1Details[0]
	scAnimDetail = aAnimDetails[0]
	exportModelWithDetail(scmdlDetail, scmdlData[scmdlDetail.baseOffset : scmdlDetail.baseOffset + scmdlDetail.size], "scmdl_", scAnimDetail)
			
	return 1


def info2Handler(bs, sectionInfos):
	mi1Data = readRelativeFile(r"DAT\MAPINFO1.BIN")
	rmdlData = readRelativeFile(r"MDL\RMDL.PAK")
	if not mi1Data:
		print("Failed to load MAPINFO1 data.")
		return 0
	if not rmdlData:
		print("Failed to load RMDL data.")
		return 0

	mi1Bs = NoeBitStream(mi1Data)	
	mi1Bs.seek(4, NOESEEK_ABS)
	mi1SectionCount = (mi1Bs.readUInt() - 8) // 8
	mi1SectionInfos = [(mi1Bs.readUInt(), mi1Bs.readUInt()) for _ in range(mi1SectionCount)]

	model1Details = readModelDetails(mi1Bs, mi1SectionInfos[MIF_TMP_ID_MLIST1])
	rAnimDetails = readAnimDetails(mi1Bs, mi1SectionInfos[MIF_TMP_ID_RANIMSEQ])

	print("Extracting room models.")
	roomBs = NoeBitStream(readSectionData(bs, sectionInfos[MIF_ID_ROLIST]))
	roomModelCount = 0
	while not roomBs.checkEOF():
		room = RoomModels(roomBs)
		for roomModel in room.roomModels:
			modelData = rmdlData[roomModel.offset : roomModel.offset + roomModel.size]
			modelDetail = model1Details[roomModel.id] if roomModel.id >= RCHR_ID_BASE and roomModel.id < RCHR_ID_TAIL else None
			animDetail = rAnimDetails[roomModel.id - RCHR_ID_BASE] if modelDetail else None
			exportModelWithDetail(modelDetail, modelData, "room_" if modelDetail else "room_model_%04i"%roomModelCount, animDetail)
			roomModelCount += 1

	return 1


def infoSystemHandler(bs, sectionInfos):
	imdlData = readRelativeFile(r"MDL\IMDL.PAK")
	shopDatas = []
	while True:
		shopData = readRelativeFile(r"MDL\SHOP%02i.PAK"%len(shopDatas))
		if not shopData:
			break
		shopDatas.append(shopData)
	
	if not imdlData:
		print("Failed to load IMDL data.")
		return 0
	if len(shopDatas) == 0:
		print("Failed to load any SHOP data.")
		return 0

	modelItemDetails = readModelDetails(bs, sectionInfos[SBI_ID_ITEMLIST])
	modelShopDetails = readModelDetails(bs, sectionInfos[SBI_ID_SHOPITEM])

	print("Extracting item models.")
	exportModelDetailSet(modelItemDetails, imdlData, -1, "item_")

	print("Extracting shop models.")
	for modelDetail in modelShopDetails:
		if modelDetail.setIndex < len(shopDatas):
			shopData = shopDatas[modelDetail.setIndex]
			modelData = shopData[modelDetail.baseOffset : modelDetail.baseOffset + modelDetail.size]
			exportModelWithDetail(modelDetail, modelData, "shop_")
		else:
			print("Error: Shop model set is out of range for loaded shop data:", modelDetail.setIndex)
	
	return 1


def mapInfoExtract(fileName, fileLen, justChecking):
	if fileLen <= 8:
		return 0

	infoHandlers = {
		"mapinfo1.bin" : (MIF_TMP_ID_COUNT, info1Handler, 0x00100004E4942),
		"mapinfo2.bin" : (MIF_ID_COUNT, info2Handler, 0x00080004E4942),
		"system.bin" : (SBI_ID_COUNT, infoSystemHandler, 0x00100004E4942)
	}

	name = localPathLower()
	if name not in infoHandlers:
		return 0

	sectionCount, mapInfoHandler, expectIdAndIndexSize = infoHandlers[name]
	with open(fileName, "rb") as f:
		idAndIndexSize = noeUnpack("<Q", f.read(8))[0]
		if idAndIndexSize != expectIdAndIndexSize:
			return 0

		if justChecking:
			return 1 #we're only in here to confirm the data

		f.seek(0, os.SEEK_SET)
		bs = NoeBitStream(f.read())

		bs.seek(8, NOESEEK_ABS)
		sectionInfos = [(bs.readUInt(), bs.readUInt()) for _ in range(sectionCount)]
		return mapInfoHandler(bs, sectionInfos)


localPathLower = lambda: rapi.getLocalFileName(rapi.getLastCheckedName()).lower()


def bonesFromChuHie(hieNodes, hieMats):
	bones = []
	for boneIndex in range(len(hieNodes)):
		hieNode = hieNodes[boneIndex]
		hieMat = hieMats[boneIndex]
		bones.append(NoeBone(boneIndex, "bone%04i"%boneIndex, hieNode.localMat.toMat43().transpose(), None, hieNode.parentIndex))
	#put the bone transforms in modelspace on the way out
	return rapi.multiplyBones(bones)


def transformFromChuTRS(trn, rot, scl = None):
	mat = NoeMat44()

	#we're replicating the original math here. we could do this instead to avoid the transpose:
	"""
	mat = mat.rotate(rot[0] * noesis.g_flRadToDeg, (1.0, 0.0, 0.0))
	mat = mat.rotate(-rot[1] * noesis.g_flRadToDeg, (0.0, 1.0, 0.0))
	mat = mat.rotate(rot[2] * noesis.g_flRadToDeg, (0.0, 0.0, 1.0))
	"""
	#however, i'm mirroring the game's conventions wherever possible.

	mat = mat.rotate(-rot[2] * noesis.g_flRadToDeg, (0.0, 0.0, 1.0))
	mat = mat.rotate(rot[1] * noesis.g_flRadToDeg, (0.0, 1.0, 0.0))
	mat = mat.rotate(-rot[0] * noesis.g_flRadToDeg, (1.0, 0.0, 0.0))
	mat[3] = NoeVec4((trn[0], trn[1], trn[2], 1.0))
	#note that although we have a scale, that game doesn't actually apply it to the transform, so neither do we.
	return mat


def checkChulipModel(data):
	if len(data) < 64:
		return 0
	dataOffsets = noeUnpack("<15I", data[:60])
	if dataOffsets[0] == DETAIL_HEADER_ID and dataOffsets[1] == DETAIL_HEADER_VERSION:
		return 1
	#check for loose binary with no header
	if dataOffsets[0] == 0 or max(dataOffsets) >= len(data):
		return 0
	return 1
	
	
def createTexture(texIndex, texList, texIndexMap, pixelData, clutData, gsTex0, texWidth, texHeight, clutWidth, clutHeight, allowUntwiddle):
	pixelFormat = (gsTex0 >> 20) & 0x3F
	clutFormat = (gsTex0 >> 51) & 0x0F
	decodedRgba = None

	#the formats in here are the only ones i've noticed so far in testing, but it's possible that more could be used
	if len(clutData) > 0:
		rgbaClut = None
		if clutFormat == GS_PSMCT16:
			#the game defaults to rendering everything with the GS_TEXA expanding bit set. this means that if the alpha bit is set in the palette, we always want to be opaque.
			#if it's not set, however, we still want to be opaque unless the color value is 0. to treat the alpha bit as a pure transparency bit, we modify the data before expanding:
			clutData = bytearray(clutData)
			for colorOffset in range(0, len(clutData), 2):
				if clutData[colorOffset] or clutData[colorOffset + 1]:
					clutData[colorOffset + 1] |= 0x80
			rgbaClut = rapi.imageDecodeRaw(clutData, clutWidth, clutHeight, "r5g5b5a1")

		if rgbaClut:
			bpp = 4 if pixelFormat == GS_PSMT4 else 8
			if allowUntwiddle:
				twiddleMapping = TWIDDLE_MAPPING_4 if bpp == 4 else TWIDDLE_MAPPING_8
				for testWidth, testHeight, writeWidth, writeHeight in twiddleMapping:
					if testWidth == texWidth and testHeight == texHeight:
						pixelData = rapi.imagePS2WriteAndReadback32(pixelData, writeWidth, writeHeight, texWidth, texHeight, bpp)
						break
			decodedRgba = rapi.imageDecodeRawPal(pixelData, rgbaClut, texWidth, texHeight, bpp, "r8g8b8a8")
		else:
			print("Warning: Unhandled CLUT format:", clutFormat)					
	else:
		if pixelFormat == GS_PSMCT32:
			#rgba 1:1, but we still need to correct for the 0..128 alpha range
			decodedRgba = rapi.imageScaleRGBA32(pixelData, (1.0, 1.0, 1.0, 255.0 / 128.0), texWidth, texHeight)
		else:
			print("Warning: Unhandled non-palettized pixel format:", pixelFormat)
			
	if not decodedRgba:
		#stub in some default data if we failed to load
		decodedRgba = bytearray(texWidth * texHeight * 4)

	tex = NoeTexture("chutex%02i"%len(texList), texWidth, texHeight, decodedRgba, noesis.NOESISTEX_RGBA32)
	tex.flags |= noesis.NTEXFLAG_WRAP_CLAMP
	tex.chuUsesClut = len(clutData) > 0
	if texIndex >= 0:
		texIndexMap[texIndex] = len(texList)
	texList.append(tex)
	
	
DEP_INDEX_MAPINFO1 = 0
DEP_INDEX_MAPINFO2 = 1
DEP_INDEX_SYSTEM = 2
DEP_INDEX_MAPTEX = 3
DEP_INDEX_SYSTEX = 4
DEP_LOAD_LIST = (r"DAT\MAPINFO1.BIN", r"DAT\MAPINFO2.BIN", r"DAT\SYSTEM.BIN", r"DAT\MAPTEX.BIN", r"DAT\SYSTEX.BIN")

#taken from more hardcoded tables in the executable. for our purposes, we only have to care about the map info type and id.
TEX_PACKAGE_MAP_INFO = (
	(MIF_TMP_ID_TEX_LS_TEX, 0),
	(MIF_TMP_ID_TEX_LS_CLUT, 0),
	(0, -1),
	(1, -1),
	(2, -1),
	(3, -1),
	(4, -1),
	(5, -1),
	(MIF_TMP_ID_TEX_ANIM0_TEX, 0),
	(MIF_TMP_ID_TEX_ANIM0_CLUT, 0),
	(MIF_TMP_ID_TEX_ANIM1_TEX, 0),
	(MIF_TMP_ID_TEX_ANIM1_CLUT, 0),
	(MIF_TMP_ID_TEX_ANIM2_TEX, 0),
	(MIF_TMP_ID_TEX_ANIM2_CLUT, 0),
	(MIF_TMP_ID_TEX_ANIM3_TEX, 0),
	(MIF_TMP_ID_TEX_ANIM3_CLUT, 0),
	(MIF_TMP_ID_TEX_ANIM4_TEX, 0),
	(MIF_TMP_ID_TEX_ANIM4_CLUT, 0),
	(MIF_TMP_ID_TEX_ANIM5_TEX, 0),
	(MIF_TMP_ID_TEX_ANIM5_CLUT, 0),
	(MIF_TMP_ID_TEX_ANIM6_TEX, 0),
	(MIF_TMP_ID_TEX_ANIM6_CLUT, 0),
	(MIF_TMP_ID_TEX_ANIM7_TEX, 0),
	(MIF_TMP_ID_TEX_ANIM7_CLUT, 0)
)
TEX_PACKAGE_INFO = (
	(0, -1),
	(1, -1),
	(2, -1),
	(3, -1),
	(SBI_ID_TEX_CLEAR_TEX, 2),
	(4, -1),
	(5, -1),
	(6, -1),
	(7, -1),
	(8, -1),
	(9, -1),
	(10, -1),
	(11, -1),
	(SBI_ID_TEX_SHOP_TEX, 2),
	(SBI_ID_TEX_SHOP_CLUT, 2),
	(SBI_ID_TEX_HINT_TEX, 2),
	(SBI_ID_TEX_HINT_CLUT, 2),
	(SBI_ID_TEX_WHOUSE_TEX, 2),
	(SBI_ID_TEX_WHOUSE_CLUT, 2),
	(SBI_ID_TEX_GAMEOVER_TEX, 2),
	(SBI_ID_TEX_GAMEOVER_CLUT, 2),
	(SBI_ID_TEX_SAVEWIN_TEX, 2),
	(SBI_ID_TEX_SAVEWIN_CLUT, 2),
	(SBI_ID_TEX_MEZAWIN_TEX, 2),
	(SBI_ID_TEX_MEZAWIN_CLUT, 2),
	(12, -1),
	(13, -1),
	(14, -1),
	(15, -1),
	(16, -1),
	(17, -1),
	(18, -1)
)

#this class manages loading of shared textures. all of this functionality can be culled if you don't care about loading faces and such.
class SharedTextureContext:
	def __init__(self):
		self.binFiles = []
		for loadPath in DEP_LOAD_LIST:
			data = readRelativeFile(loadPath, 8)
			if not data:
				print("Warning: Shared textures will not be loaded, failed to find data on path for", loadPath)
				break
			self.binFiles.append(data)
		self.isValid = len(self.binFiles) == len(DEP_LOAD_LIST)
		if self.isValid:			
			self.streams = [NoeBitStream(data) for data in self.binFiles]
			self.fileSections = []
			for bs in self.streams:
				bs.seek(4, NOESEEK_ABS)
				sectionCount = (bs.readUInt() - 8) // 8
				sectionInfos = [(bs.readUInt(), bs.readUInt()) for _ in range(sectionCount)]
				self.fileSections.append(sectionInfos)
				
			texAnimBs = NoeBitStream(readSectionData(self.streams[DEP_INDEX_MAPINFO2], self.fileSections[DEP_INDEX_MAPINFO2][MIF_ID_TALIST]))
			texAnimCount = len(texAnimBs.getBuffer()) // TexAnim.DataSize
			self.texAnims = [TexAnim(texAnimBs) for _ in range(texAnimCount)]
	
	def readData(self, resId):
		isPerMap = (resId & TEX_MAP_FLAG) != 0
		texPkgList = TEX_PACKAGE_MAP_INFO if isPerMap else TEX_PACKAGE_INFO
		pkgInfoIndex = resId & TEX_MAP_MASK
		if pkgInfoIndex >= len(texPkgList):
			return None
		
		pkgSectionIndex, pkgType = texPkgList[pkgInfoIndex]
		typeToIndex = { 0 : DEP_INDEX_MAPINFO1, 1 : DEP_INDEX_MAPINFO2, 2 : DEP_INDEX_SYSTEM }
		pkgIndex = typeToIndex.get(pkgType, DEP_INDEX_MAPTEX if isPerMap else DEP_INDEX_SYSTEX)
		pkgSections = self.fileSections[pkgIndex]
		if pkgSectionIndex >= len(pkgSections):
			return None
		return readSectionData(self.streams[pkgIndex], pkgSections[pkgSectionIndex])
	
	def createSharedTexture(self, texIndex, texList, texIndexMap, texAnimId):
		if not self.isValid or texAnimId < 0 or texAnimId >= len(self.texAnims):
			return False
		texAnim = self.texAnims[texAnimId]
		pixelData = self.readData(texAnim.texId)
		clutData = self.readData(texAnim.clutId)
		if not pixelData or not clutData:
			return False
		
		pixelDataSize = texAnim.texSize
		clutDataSize = texAnim.clutSize
		texCount = len(pixelData) // pixelDataSize
		clutCount = len(clutData) // clutDataSize
		#these shared textures are always 4bpp, so we can hardcode the format.
		#shared textures are also never twiddled.
		gsTex0 = (GS_PSMT4 << 20) | (GS_PSMCT16 << 51)
		if LOAD_ALL_ANIM_TEXTURES:
			for subTexIndex in range(0, texCount):
				pixelOffset = subTexIndex * pixelDataSize
				clutOffset = subTexIndex * clutDataSize
				subClut = clutData[clutOffset : clutOffset + clutDataSize] if clutCount >= texCount else clutData
				createTexture(texIndex if subTexIndex == 0 else -1, texList, texIndexMap, pixelData[pixelOffset : pixelOffset + texAnim], subClut, gsTex0, texAnim.width, texAnim.height, 8, 2, False)
			texList[texIndex].chuTexCount = texCount
		else:
			if texAnim.srcId < texCount and texAnim.srcId < clutCount:
				pixelOffset = texAnim.srcId * pixelDataSize
				clutOffset = texAnim.srcId * clutDataSize
				pixelData = pixelData[pixelOffset : pixelOffset + pixelDataSize]
				clutData = clutData[clutOffset : clutOffset + clutDataSize]
				
			createTexture(texIndex, texList, texIndexMap, pixelData, clutData, gsTex0, texAnim.width, texAnim.height, 8, 2, False)
			
		return True


def loadChulipModel(data, mdlList):
	bs = NoeBitStream(data)

	animSequences = []
	hasDetailHeader = False
	texturesAreShared = False
	if bs.readUInt() == DETAIL_HEADER_ID:
		hasDetailHeader = True
		bs.readUInt() #version
		if bs.readUInt():
			bs.readUInt() #modelIndex, not currently used on import
			texturesAreShared = bs.readUInt() != 0
			texShareInfo = [ModelTexShareInfo(bs) for _ in range(8)]

		if bs.readUInt():
			seqCount = bs.readUInt()
			animSequences = [(bs.readUInt(), bs.readUInt()) for _ in range(seqCount)]

		#cut the header off after we're done reading it
		bs = NoeBitStream(data[bs.tell():])

		if len(animSequences) > 0:
			#just print out the start/end frames for reference
			print("Anim sequence data is present:", animSequences)
	else:
		bs.seek(0, NOESEEK_ABS)
	hdr = FWDataHeader(bs)

	ctx = rapi.rpgCreateContext()
	rapi.rpgSetOption(noesis.RPGOPT_TRIWINDBACKWARD, 1)

	bs.seek(hdr.shapeOffset, NOESEEK_ABS)
	shapeData = FWShapeData(bs)		
	shapes = []
	for shapeOffset in shapeData.shapeOffsets:
		bs.seek(shapeOffset, NOESEEK_ABS)
		shapes.append(FWShape(bs))

	bones = []
	if hdr.baseMatrixOffset and hdr.hieOffset:
		bs.seek(hdr.hieOffset + 12, NOESEEK_ABS)
		boneCount = bs.readInt()
		hieNodes = [FWHierarchyBone(bs) for _ in range(boneCount)]
		bs.seek(hdr.baseMatrixOffset + 16, NOESEEK_ABS)
		hieMats = [FWHierarchyMat(bs) for _ in range(boneCount)]
		bones = bonesFromChuHie(hieNodes, hieMats)

	kfAnims = []

	texList = []
	mtlList = []

	texIndexMap = {}
	mtlSet = set()

	if hdr.texOffset:
		sharedTexContext = SharedTextureContext() if texturesAreShared and ALLOW_SHARED_TEXTURE_LOAD else None
	
		bs.seek(hdr.texOffset + 12, NOESEEK_ABS)
		texCount = bs.readInt()

		texShareIndex = 0		
		for texIndex in range(texCount):
			gsTex0 = bs.readUInt64()
			bs.readUInt64() #unused
			pixelDataSize = ((bs.readUInt() + 3) & ~3) << 2
			clutDataSize = ((bs.readUInt() + 3) & ~3) << 2
			texWidth = bs.readUShort()
			texHeight = bs.readUShort()
			clutWidth = bs.readUShort()
			clutHeight = bs.readUShort()
			#decWidth = 1 << ((gsTex0 >> 26) & 0x0F)
			#decHeight = 1 << ((gsTex0 >> 30) & 0x0F)
			
			pixelData = bs.readBytes(pixelDataSize)
			clutData = bs.readBytes(clutDataSize)
			
			isSharedTexture = False
			#whether the textures should be shared or not, they're present in the file here. however, the data itself is usually something like a stub 8x8 texture.
			if texturesAreShared and texShareIndex < len(texShareInfo):
				texShare = texShareInfo[texShareIndex]
				if texShare.texDstId == texIndex:
					if sharedTexContext:
						isSharedTexture = sharedTexContext.createSharedTexture(texIndex, texList, texIndexMap, texShare.texAnimManId)
						if not isSharedTexture:
							print("Shared texture not loaded:", texIndex, "maps to", texShare.texAnimManId)
					texShareIndex += 1

			if not isSharedTexture:
				createTexture(texIndex, texList, texIndexMap, pixelData, clutData, gsTex0, texWidth, texHeight, clutWidth, clutHeight, True)

	if len(bones) > 0:
		if hdr.animOffset and hdr.animKfOffset and hdr.animKvOffset:
			#we've got some anim data in addition to a skeleton, let's process it
			bs.seek(hdr.animOffset + 12, NOESEEK_ABS)
			animBoneCount = bs.readInt()
			animBones = [FWAnimBone(bs) for _ in range(animBoneCount)]
			
			bs.seek(hdr.animKfOffset + 12, NOESEEK_ABS)
			kfCount = bs.readInt()
			animKfs = [FWAnimKeyTime(bs) for _ in range(kfCount)]
			
			bs.seek(hdr.animKvOffset + 12, NOESEEK_ABS)
			kvCount = bs.readInt()
			animKvs = [FWAnimKeyValue(bs) for _ in range(kvCount)]

			#now convert the data for the noesis keyframe evaluator.
			frameToTime = 1.0 / CHULIP_ANIM_EVAL_FRAMERATE
			kfBones = []
			for animBone in animBones:
				kfBone = NoeKeyFramedBone(animBone.boneIndex)
				kfRot = []
				kfTrans = []

				animKf = animKfs[animBone.kfIndex]
				animKv = animKvs[animBone.kvIndex]
				for frameIndex in range(animBone.keyCount):
					time = animKf.times[frameIndex] * frameToTime
					valueIndex = frameIndex << 3
					trn = animKv.values[valueIndex : valueIndex + 4]
					rot = animKv.values[valueIndex + 4 : valueIndex + 8]
					mat = transformFromChuTRS(trn, rot).toMat43().transpose()
					kfRot.append(NoeKeyFramedValue(time, mat.toQuat()))
					kfTrans.append(NoeKeyFramedValue(time, mat[3]))

				kfBone.setRotation(kfRot)
				kfBone.setTranslation(kfTrans)
				kfBones.append(kfBone)
				
			kfAnim = NoeKeyFramedAnim("chulip_anims", bones, kfBones, CHULIP_ANIM_EVAL_FRAMERATE)
			kfAnims.append(kfAnim)

		#fill in default weights
		for boneIndex in range(len(bones)):
			shapeIndex = hieMats[boneIndex].shapeIndex
			if shapeIndex >= 0 and shapeIndex < len(shapes):
				shape = shapes[shapeIndex]
				for draw in shape.draws:
					for geo in draw.geos:
						geo.weightIndexData = bytearray(noePack("<%iI"%geo.vertCount, *([boneIndex] * geo.vertCount)))
		
		if hdr.shareInfoOffset:
			#we've got data to share vertices across bones
			bs.seek(hdr.shareInfoOffset + 12, NOESEEK_ABS)
			shareInfoCount = bs.readInt()
			boneShareInfos = [FWPerBoneShareInfo(bs) for _ in range(shareInfoCount)]
			
			bs.seek(hdr.shareVDataOffset + 12, NOESEEK_ABS)
			sharePosCount = bs.readInt()
			sharePosData = bs.readBytes(sharePosCount * 16)
			bs.seek(sharePosCount * 16, NOESEEK_REL) #destination buffer, not needed
			
			bs.seek(hdr.shareNDataOffset + 12, NOESEEK_ABS)
			shareNrmCount = bs.readInt()
			shareNrmData = bs.readBytes(shareNrmCount * 16)
			bs.seek(shareNrmCount * 16, NOESEEK_REL) #destination buffer, not needed
			
			bs.seek(hdr.shareVOffset, NOESEEK_ABS)
			sharePosInfo = FWShareInfo(bs)
			bs.seek(hdr.shareNOffset, NOESEEK_ABS)
			shareNrmInfo = FWShareInfo(bs)

			#don't trust header counts for the indices, as the game doesn't use them.
			#these map from the shape vertex into sharePosData and shareNrmData.
			posIndexCount = sharePosInfo.calculateIndexCount()
			nrmIndexCount = shareNrmInfo.calculateIndexCount()
			bs.seek(hdr.shareVIndexOffset + 16, NOESEEK_ABS)
			sharePosIndices = [bs.readInt() for _ in range(posIndexCount)]
			bs.seek(hdr.shareNIndexOffset + 16, NOESEEK_ABS)
			shareNrmIndices = [bs.readInt() for _ in range(nrmIndexCount)]
			
			#this means that the format is limited to putting all cross-bone geometry into a single shape
			shape = shapes[sharePosInfo.shareShapeIndex]
			if sharePosInfo.shareShapeIndex != shareNrmInfo.shareShapeIndex:
				print("Error: initShareGeom indicates that shapev == shapen, but this is not the case here.")
			elif posIndexCount != shape.vertCount or nrmIndexCount != shape.vertCount:
				print("Error: Vertex map doesn't match shape vertex count.")
			else:
				#it's weird to have to do this (it's a very tenuous relationship to dstGeoIndex), but this is what initShareGeom does
				orderedGeos = []
				for draw in shape.draws:
					for geo in draw.geos:
						orderedGeos.append(geo)

				weightIndices = bytearray(noePack("<%iI"%sharePosCount, *([0] * sharePosCount)))

				#run through and modify the weight indices using the per-bone data.
				for boneIndex in range(min(len(bones), len(boneShareInfos))):
					boneShareInfo = boneShareInfos[boneIndex]
					if boneShareInfo.posCount > 0 or boneShareInfo.nrmCount > 0:
						for posIndex in range(boneShareInfo.posCount):
							weightIndexOffset = ((boneShareInfo.posIndex + posIndex) << 2)
							weightIndices[weightIndexOffset : weightIndexOffset + 4] = noePack("<I", boneIndex)

				#now map the shared data back into the shape vertices. we copy positions/normals from the shared data in addition to updating the (now actually per-vertex) weight indices.
				for section in sharePosInfo.sections:
					geo = orderedGeos[section.dstGeoIndex]
					for vertIndex in range(section.vertCount):
						srcIndex = sharePosIndices[vertIndex]
						posOffset = (vertIndex << 4)
						sharePosOffset = (srcIndex << 4)
						geo.posData[posOffset : posOffset + 16] = sharePosData[sharePosOffset : sharePosOffset + 16]

						weightOffset = (vertIndex << 2)
						shareWeightOffset = (srcIndex << 2)
						geo.weightIndexData[weightOffset : weightOffset + 4] = weightIndices[shareWeightOffset : shareWeightOffset + 4]

				for section in shareNrmInfo.sections:
					geo = orderedGeos[section.dstGeoIndex]
					for vertIndex in range(section.vertCount):
						srcIndex = shareNrmIndices[vertIndex]
						nrmOffset = (vertIndex << 4)
						shareNrmOffset = (srcIndex << 4)
						geo.nrmData[nrmOffset : nrmOffset + 16] = shareNrmData[shareNrmOffset : shareNrmOffset + 16]

	for shape in shapes:
		for draw in shape.draws:
			draw.renderToContext(texList, texIndexMap, mtlList, mtlSet)

	if len(bones) > 0:
		#this will transform all of the geometry from local space onto the skeleton
		rapi.rpgSkinPreconstructedVertsToBones(bones)

	rapi.rpgOptimize()
	mdl = rapi.rpgConstructModel()
	if mdl:
		mdl.setBones(bones)
		mdl.setAnims(kfAnims)
		if len(texList) > 0 or len(mtlList) > 0:
			mdl.setModelMaterials(NoeModelMaterials(texList, mtlList))
		mdlList.append(mdl)
		rapi.setPreviewOption("setAngOfs", "0 270 270")
		rapi.setPreviewOption("setAnimSpeed", str(CHULIP_ANIM_PLAYBACK_FRAMERATE))
		if USE_PBR_MATERIALS:
			rapi.setPreviewOption("autoLoadNonDiffuse", "1")
	
	return 1
