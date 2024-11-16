from inc_noesis import *
from inc_atarijaguar import JagUtils
from fmt_atarijaguar_cry import CryImage

CYBERMORPH_HASH = bytes((0xA0, 0x10, 0xA7, 0x31, 0x7B, 0x4E, 0xCA, 0x54, 0xE3, 0xD8, 0x5A, 0xFB, 0x0F, 0x61, 0xA5, 0x2C))

GRAPHICS_BASE_OFFSET = 0xFFB04 #starting with nebula2
GRAPHICS_COUNT = 64

HUD_OFFSET = 0xC7886
HUD_PAL_OFFSET = 0xC8CFC
HUD_WIDTH = 320
HUD_HEIGHT = 53

MODELS_BASE_OFFSET = 0xE32DA #starting with drone1
MODELS_COUNT = 176

WORLDS_BASE_OFFSET = 0xD96D4 #starting with f18
WORLDS_COUNT = 53

FIND_PULSE_COLOR = False
FIND_MORPHS = False
USE_FACE_NORMALS = True

def registerNoesisTypes():
	handle = noesis.register("Cybermorph ROM", ".j64")
	noesis.setHandlerExtractArc(handle, cmExtractArc)
	
	handle = noesis.register("Cybermorph Image", ".cmjag_grobj")
	noesis.setHandlerTypeCheck(handle, grobjCheckType)
	noesis.setHandlerLoadRGBA(handle, grobjLoadRGBA)
	
	handle = noesis.register("Cybermorph Model", ".cmjag_3dobj")
	noesis.setHandlerTypeCheck(handle, mdlCheckType)
	noesis.setHandlerLoadModel(handle, mdlLoadModel)
	
	return 1

class GraphicsFrame:
	def __init__(self, bs):
		self.width = bs.readUShort()
		self.height = bs.readUShort()
		self.yOffset = bs.readUShort()
		self.offset = bs.readUShort()
		self.dataOffset = bs.tell()

class GraphicsObject:
	Type_Frame = 0
	def __init__(self, bs, type):
		self.type = type
		self.blitterFlags1 = bs.readUInt()
		self.blitterFlags2 = bs.readUInt()
		self.blitterCmd = bs.readUInt()
		self.phraseAdj = bs.readUShort()
		self.frames = []
		if type == GraphicsObject.Type_Frame:
			frame = GraphicsFrame(bs)
			self.frames.append(frame)

	def isValid(self, dataSize):
		if self.type == GraphicsObject.Type_Frame:
			if len(self.frames) > 0:
				frame = self.frames[0] #just validate first frame
				phraseGap, pixelSize, zOffset, decWidth = JagUtils.decodeBlitterFlags(self.blitterFlags2)
				#doesn't hold true for all graphics objects
				#return decWidth == frame.width
				imageSize = (frame.width * frame.height * pixelSize + 7) // 8
				return dataSize >= (frame.dataOffset + imageSize)
		return False
		
	def decode(self, data, texList):
		for frame in self.frames:
			#just create a cry header for it
			cryHeader = noePack(">HHI", frame.width, frame.height, self.blitterFlags2)
			cry = CryImage(cryHeader + data[frame.dataOffset:], False)
			tex = cry.decode()
			if tex:
				texList.append(tex)
				
class ModelFace:
	def __init__(self, bs):
		self.flags = bs.readUShort() #2 means no shading
		vertexCount = bs.readUShort()
		self.color = bs.readBytes(2)
		self.imagePtr = bs.readUInt() #always 0
		self.indices = [bs.readShort() for x in range(vertexCount)]

class ModelObject:
	def __init__(self, bs):
		self.faces = []
		try:
			self.pointCount = bs.readUShort()
			self.normalCount = bs.readUShort() #generally 0, per-vertex normals are ignored by the game even though a field exists for them
			self.faceNormalCount = bs.readUShort()
			self.vertexCount = bs.readUShort()
			self.faceNormalBaseIndex = self.normalCount
			self.posBaseIndex = self.faceNormalBaseIndex + self.faceNormalCount
			self.pointData = [bs.readShort() for x in range(self.pointCount * 4)]
			faceCount = bs.readUShort()
			for faceIndex in range(faceCount):
				face = ModelFace(bs)
				for index in face.indices:
					if index < 0 or index >= self.vertexCount:
						noesis.doException("Bad poly index")
						break
				self.faces.append(face)
			self.defaultMaterialName = "cybermorph_mtl"
		except:
			self.pointCount = 0
			
	def isValid(self):
		return self.pointCount > 0 and len(self.faces) > 0

	def createDefaultMaterialData(self):
		noeMat = NoeMaterial(self.defaultMaterialName, "")
		noeMat.setTexture(noesis.getScenesPath() + "sample_pbr_o.png")
		noeMat.setSpecularTexture(noesis.getScenesPath() + "sample_pbr_o.png")
		noeMat.setEnvTexture(noesis.getScenesPath() + "sample_pbr_e.dds")
		noeMat.flags |= noesis.NMATFLAG_PBR_METAL | noesis.NMATFLAG_PBR_SPEC_IR_RG
		noeMat.flags2 |= noesis.NMATFLAG2_PREFERPPL
		noeMat.setMetal(0.0, 1.0)
		noeMat.setRoughness(0.0, 0.7)
		noeMat.setDefaultBlend(0)
		return NoeModelMaterials([], [noeMat])
		
	def feedMorphTargets(self):
		frameData = bytearray()
		for vertIndex in range(self.vertexCount):
			frameData += noePack("<fff", *self.getVertexPos(vertIndex))
		rapi.rpgFeedMorphTargetPositions(frameData, noesis.RPGEODATA_FLOAT, 12)
		if USE_FACE_NORMALS and self.faceNormalCount == len(self.faces):
			#convert face normals back to per-vertex to feed in as morph frames
			frameNormalData = bytearray()
			vertToFace = [0] * self.vertexCount
			for faceIndex in range(len(self.faces)):
				face = self.faces[faceIndex]
				for index in face.indices:
					vertToFace[index] = faceIndex
					
			for vertIndex in range(self.vertexCount):
				frameNormalData += noePack("<fff", *self.getVertexNormal(vertToFace[vertIndex]))
			rapi.rpgFeedMorphTargetNormals(frameNormalData, noesis.RPGEODATA_FLOAT, 12)
	
		rapi.rpgCommitMorphFrame(self.vertexCount)
		
	def getVertexPos(self, index):
		absIndex = self.posBaseIndex + index
		return self.pointData[absIndex * 4 : absIndex * 4 + 3]
		
	def getVertexNormal(self, faceIndex):
		absIndex = self.faceNormalBaseIndex + faceIndex
		v = NoeVec3([float(v) for v in self.pointData[absIndex * 4 : absIndex * 4 + 3]])
		v = v.normalize()
		return v.getStorage()

	def drawModel(self, mdlList):
		ctx = rapi.rpgCreateContext()

		morphMdls = []
		#let's have a little fun
		if FIND_MORPHS:
			fn = rapi.getLastCheckedName()
			if fn.lower().endswith("mdl0132.cmjag_3dobj"):
				morphPath, baseName = os.path.split(fn)
				mdlIndex = 133
				while mdlIndex <= 173:
					morphName = os.path.join(morphPath, "mdl%04i.cmjag_3dobj"%mdlIndex)
					if os.path.exists(morphName):
						with open(morphName, "rb") as mF:
							morphMdl = ModelObject(NoeBitStream(mF.read(), NOE_BIGENDIAN))
							if morphMdl.isValid() and morphMdl.vertexCount == self.vertexCount:
								morphMdls.append(morphMdl)
					mdlIndex += 1

		rapi.rpgSetName("cybermesh")
		rapi.rpgSetMaterial(self.defaultMaterialName)
		
		if len(morphMdls) > 0:
			for morphMdl in morphMdls:
				morphMdl.feedMorphTargets()
			rapi.rpgCommitMorphFrameSet()
		
		feedNormals = USE_FACE_NORMALS and self.faceNormalCount == len(self.faces)
		
		for faceIndex in range(len(self.faces)):
			face = self.faces[faceIndex]
			rapi.immBegin(noesis.RPGEO_POLYGON)
						
			if feedNormals:
				rapi.immNormal3(self.getVertexNormal(faceIndex))
						
			if FIND_PULSE_COLOR and face.color == b"\0\0":
				color = [2.0, 0.25, 0.0, 1.0]
			else:
				color = [float(c) / 255.0 for c in noeUnpack("BBBB", JagUtils.cryToRgba32(face.color))]
			rapi.immColor4(color)
			for index in face.indices:
				if len(morphMdls) > 0:
					rapi.immVertMorphIndex(index)
				rapi.immVertex3(self.getVertexPos(index))
			rapi.immEnd()
		
		rapi.rpgOptimize()
		if not USE_FACE_NORMALS:
			rapi.rpgSmoothNormals()
		mdl = rapi.rpgConstructModel()
		mdl.setModelMaterials(self.createDefaultMaterialData())
		
		rapi.setPreviewOption("autoLoadNonDiffuse", "1")
		if len(morphMdls) > 0:
			rapi.setPreviewOption("setAnimSpeed", "2.0")
	
		mdlList.append(mdl)
		
def grobjCheckType(data):
	if len(data) < 22:
		return 0
	grobj = GraphicsObject(NoeBitStream(data, NOE_BIGENDIAN), GraphicsObject.Type_Frame)
	return 1 if grobj.isValid(len(data)) else 0
	
def grobjLoadRGBA(data, texList):
	grobj = GraphicsObject(NoeBitStream(data, NOE_BIGENDIAN), GraphicsObject.Type_Frame)
	grobj.decode(data, texList)
	return 1
	
def mdlCheckType(data):
	if len(data) < 8:
		return 0
	mdl = ModelObject(NoeBitStream(data, NOE_BIGENDIAN))
	return 1 if mdl.isValid() else 0

def mdlLoadModel(data, mdlList):
	mdl = ModelObject(NoeBitStream(data, NOE_BIGENDIAN))
	mdl.drawModel(mdlList)
	return 1

def cmGetFileData(currentOffset, bs):
		bs.seek(currentOffset, NOESEEK_ABS)
		type = bs.readUShort()
		dstSize = bs.readUInt()
		buffer = bs.getBuffer()
		currentOffset = bs.tell()
		if type > 0:
			#ancient gt compression (might be used as-is in some other games, words are still little-endian)
			data = rapi.callExtensionMethod("ungt_decomp", buffer[currentOffset:], dstSize, 1)
			currentOffset += rapi.callExtensionMethod("ungt_decomp_src_size", buffer[currentOffset:], 1)
		else:
			#not compressed
			data = buffer[currentOffset : currentOffset + dstSize]
			currentOffset += dstSize
		currentOffset = ((currentOffset + 1) & ~1)
		while buffer[currentOffset] != 0:
			currentOffset += 1
		return currentOffset, data

def cmDumpFiles(baseOffset, count, bs, filePrefix, fileExt):
	currentOffset = baseOffset
	for fileIndex in range(count):
		currentOffset, data = cmGetFileData(currentOffset, bs)
		name = filePrefix + "%04i"%fileIndex + fileExt
		print("Writing", name)
		rapi.exportArchiveFile(name, data)
	
def cmExtractArc(fileName, fileLen, justChecking):
	if fileLen <= JagUtils.DefaultBootCodeSize:
		return 0

	try:
		with open(fileName, "rb") as f:
			data = f.read(JagUtils.DefaultBootCodeSize)

			if data[0] != 0xF6:
				return 0
			#we could just calculate our own checksum, but what fun would that be?
			checksum = JagUtils.bootCodeChecksum(data[:JagUtils.DefaultBootCodeSize])				
			if checksum != CYBERMORPH_HASH:
				return 0

			if justChecking:
				return 1

			f.seek(0, os.SEEK_SET)
			bs = NoeBitStream(f.read(), NOE_BIGENDIAN)
	except:
		return 0
	
	cmDumpFiles(GRAPHICS_BASE_OFFSET, GRAPHICS_COUNT, bs, "gfx", ".cmjag_grobj")		
	
	hudEncWidth = JagUtils.closestTextureWidth(HUD_WIDTH)
	hudHeader = noePack(">IIIHHHHH", 0x10000 | hudEncWidth, 0x10018 | hudEncWidth, 0x401, 0, HUD_WIDTH, HUD_HEIGHT, 0, 0)
	x, hudData = cmGetFileData(HUD_OFFSET, bs)
	x, hudPalData = cmGetFileData(HUD_PAL_OFFSET, bs)
	hudName = "hud.cmjag_grobj"
	print("Writing", hudName)
	rapi.exportArchiveFile(hudName, hudHeader + hudData + noePack(">H", 256) + hudPalData)

	cmDumpFiles(MODELS_BASE_OFFSET, MODELS_COUNT, bs, "mdl", ".cmjag_3dobj")		

	cmDumpFiles(WORLDS_BASE_OFFSET, WORLDS_COUNT, bs, "wld", ".cmjag_wlobj")		
	
	return 1
