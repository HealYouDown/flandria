from inc_noesis import *
from inc_n64 import DisplayListContext, DLMaterialEncapsulation, StandardVertex, DL_UCODEMODE_UC5, TILEIMG_COLORFMT_CI, TILEIMG_BPP_SIZES
import math

#this was written to grab models out of a bunch of loose object files, but the anim, draw data, etc. specs probably apply to the retail ROM too

MEM_SIZE = 0x8000000
EYE_TEX_COUNT = 8
MOUTH_TEX_COUNT = 6
DEFAULT_FRAMERATE = 30.0
OLD_NPC = False #set to true to load "old" npc data
OLD_NPC_FACE_TEX_INDEX = 1 #specifies which face texture to try to write into scratch area when loading old npc's
DUMP_ADDITIONAL_MODELS = False #don't default to dumping models outside of the draw data unless no draw data was found
LOAD_ALL_ANIMS = False #probably don't want to do this unless you've isolated a model out
FORCE_ADDITIONAL_TEXTURE_WIDTH = 32 #when loading loose textures, setting this to 0 will guess the width from the texel count instead, but may often be wrong
ADDITIONAL_TEXTURE_RGBA16 = False #if true, try loading textures as rgba16 instead of paletted
ONLY_LOAD_IMMEDIATE_OBJECT = False #if true, only load the object selected and don't crawl through surrounding files

SKELETON_PREFIX = "cKF_bs_"

ENABLE_MASS_DUMPER = False #enables right-click context tool to mass-dump models
MASS_DUMP_FORMAT = "gltf"
MASS_DUMP_IMPORT_OPTIONS = "-afskelanm"
MASS_DUMP_EXPORT_OPTIONS = ""

def registerNoesisTypes():
	handle = noesis.register("Animal Forest NPC Object", ".o")
	noesis.setHandlerTypeCheck(handle, elfCheckType)
	noesis.setHandlerLoadModel(handle, npcObjectLoadModel)
	noesis.addOption(handle, "-afobjanim", "prefer animation, arg=index.", noesis.OPTFLAG_WANTARG)
	noesis.addOption(handle, "-afskelanm", "take first anim frame (if available) for skeleton.", 0)
	noesis.addOption(handle, "-afusecolors", "apply colors and don't interpret as normals.", 0)
	noesis.addOption(handle, "-afnodups", "avoid duplicate/variant characters in draw list.", 0)
	if ENABLE_MASS_DUMPER:
		handle = noesis.registerTool("Animal Forest NPC Dumper", afMassDump, "Scans down tree around selected object and dumps all found AF models/textures.")
		noesis.setToolFlags(handle, noesis.NTOOLFLAG_CONTEXTITEM)
		noesis.setToolVisibleCallback(handle, afDumpContextVisible)
	return 1

def elfCheckType(data):
	return 0 if len(data) < 4 or noeUnpack("<I", data[:4])[0] != 0x464C457F else 1

def afDumpContextVisible(toolIndex, selectedFile):
	if not selectedFile:
		return 0
	nameNoExt, ext = os.path.splitext(selectedFile)
	ext = ext.lower()
	if ext != ".o":
		return 0
	return 1

class DrawDataEntry:
	DataSize = 100
	def __init__(self, entryIndex, data):
		bs = NoeBitStream(data, NOE_BIGENDIAN)
		self.entryIndex = entryIndex
		self.shapeBank = bs.readUShort()
		self.texBank = bs.readUShort()
		self.skelAddr = bs.readUInt()
		
		self.baseTexAddr = bs.readUInt()
		self.basePalAddr = bs.readUInt()
		self.eyeTexAddrs = [bs.readUInt() for x in range(EYE_TEX_COUNT)]
		self.mouthTexAddrs = [bs.readUInt() for x in range(MOUTH_TEX_COUNT)]
		self.eyeTexPos = bs.readInt()
		self.mouthTexPos = bs.readInt()
		self.clothTexPos = bs.readInt()
		
		self.scale = bs.readFloat()
		self.talkAnimType = bs.readInt()
		self.type = bs.readUByte()
		self.umbType = bs.readUByte()
		self.eyeOffset = bs.readUByte()
		self.melody = bs.readUByte()
		self.chkRange = bs.readShort()
		self.chkHeight = bs.readShort()
		
class JointEntry:
	DataSize = 12
	def __init__(self, jointIndex, bs):
		self.jointIndex = jointIndex
		self.dlAddr = bs.readUInt()
		self.childCount = bs.readUByte()
		self.workFlag = bs.readUByte()
		self.translation = [bs.readShort(), bs.readShort(), bs.readShort()]
		self.parentIndex = -1
		self.childList = []
		mat = NoeMat43()
		mat[3] = NoeVec3(self.translation)
		self.localTransform = mat.toMat44()
		self.isTransformed = False
	
	def transform(self, jointList):
		if self.isTransformed:
			return
		self.isTransformed = True
		if self.parentIndex >= 0:
			parentJoint = jointList[self.parentIndex]
			parentJoint.transform(jointList)
			self.modelTransform = self.localTransform * parentJoint.modelTransform
		else:
			self.modelTransform = self.localTransform

def afReadVerts(dlc, destOffset, readAddr, readSize):
	skel = dlc.getUserData()
	return skel.readVerts(dlc, destOffset, readAddr & 0x00FFFFFF, readSize)

def afDrawTris(dlc, drawList, vertexBuffer, vertexSize):
	skel = dlc.getUserData()
	mtl, tex = skel.getMaterialAndTextureForTile(dlc)
	rapi.rpgSetMaterial(mtl.name)
	meshName = "mesh%02i_"%(skel.currentNodeIndex) if skel.currentNodeIndex >= 0 else ""
	rapi.rpgSetName(meshName + mtl.name)
	
	colorAsColor = noesis.optWasInvoked("-afusecolors")
	rapi.immBegin(noesis.RPGEO_TRIANGLE)
	for tri in drawList:
		for index in tri:
			vertOffset = index * vertexSize
			vert = StandardVertex(vertexBuffer[vertOffset : vertOffset + vertexSize])
			if tex:
				st = dlc.calculateST(tex.width, tex.height, vert.st)
				rapi.immUV2(st)

			if colorAsColor:
				rapi.immColor4(vert.color)
				vertNormal = None
			else:
				#color is actually a vertex normal, convert back and unpack as signed
				nrmData = noePack("BBB", int(vert.color[0] * 255.0), int(vert.color[1] * 255.0), int(vert.color[2] * 255.0))
				nrmData = noeUnpack("bbb", nrmData)
				vertNormal = NoeVec3((nrmData[0] / 127.0, nrmData[1] / 127.0, nrmData[2] / 127.0))
				
			if skel.currentDrawIndex >= 0:
				if index in skel.vertToDrawIndex:
					boneIndex = skel.drawToBoneIndex[skel.vertToDrawIndex[index]]
					transformMat = skel.joints[boneIndex].modelTransform.toMat43()
					vert.pos = (transformMat * NoeVec3(vert.pos)).getStorage()
					if vertNormal:
						vertNormal = transformMat.transformNormal(vertNormal)
					rapi.immBoneIndex([boneIndex])
				else:
					rapi.immBoneIndex([0])
				rapi.immBoneWeight([1.0])
			if vertNormal:
				rapi.immNormal3(vertNormal.getStorage())
			rapi.immVertex3(vert.pos)
	rapi.immEnd()
	
def afReadMat(dlc, readAddr):
	skel = dlc.getUserData()
	for scratchAddr in skel.animScratchAddrs:
		if readAddr >= scratchAddr:
			readAddr -= scratchAddr
			break
	
	if readAddr & 63:
		print("Error: Expect transform reads to be matrix-aligned.")
	else:
		matIndex = readAddr // 64
		if matIndex < len(skel.drawJoints):
			skel.currentDrawIndex = matIndex
			#kinda arbitrary since we don't actually use the matrix from the dlc, but this would be the "right" thing otherwise
			return skel.drawJoints[matIndex].modelTransform
		else:
			print("Error: Matrix read out of expected range:", matIndex, "/", "%08X"%readAddr)
	return NoeMat44()
	
def afReadTMem(dlc, destOffset, readAddr, dataSize):
	if readAddr == 0:
		print("Warning: TMEM read from 0, displaylist pointer probably wasn't properly relocated.")
	skel = dlc.getUserData()
	sysMem = skel.sysMem
	skel.tmemWriteCount += 1 #track tmem writes so to avoid caching based on dirty tmem address
	if destOffset >= 0x800:
		skel.palTMemValid = True
	return sysMem[readAddr : readAddr + dataSize]
	
def afDisplayList(dlc, readAddr):
	if readAddr == 0:
		print("Warning: Branch read from 0, displaylist pointer probably wasn't properly relocated.")
		return None #don't let the branch actually occur, terrible things would probably happen
	skel = dlc.getUserData()
	sysMem = skel.sysMem
	dlSize = dlc.calculateDisplayListSize(sysMem, readAddr)	
	return sysMem[readAddr : readAddr + dlSize]
	
def afNoeBonesFromJointList(joints):
	noeBones = []
	for jointIndex in range(len(joints)):
		joint = joints[jointIndex]
		noeBone = NoeBone(jointIndex, "bone%02i"%jointIndex, joint.modelTransform.toMat43(), None, joint.parentIndex)
		noeBones.append(noeBone)
	return noeBones
	
class AFModel:
	def __init__(self, name, drawData, baseDrawAddr, sysMem, boyPalTex):
		self.name = name
		self.drawData = drawData
		self.baseDrawAddr = baseDrawAddr
		self.sysMem = sysMem
		self.boyPalTex = boyPalTex
		self.tmemWriteCount = 0
		self.joints = []
		self.displayJointCount = 0
		self.materials = []
		self.textures = []
		self.materialDict = {}
		self.currentNodeIndex = -1
		self.animScratchAddrs = []
		self.palTMemValid = False

	def readVerts(self, dlc, destOffset, readAddr, readSize):
		vertData = self.sysMem[readAddr : readAddr + readSize]
		#set up transform references so we don't have to do it here and requantize the result
		vertCount = readSize // 16
		for vertIndex in range(vertCount):
			vertOffset = vertIndex * 16
			absOffset = destOffset + vertOffset
			self.vertToDrawIndex[absOffset // 16] = self.currentDrawIndex
		return vertData

	def getMaterialAndTextureForTile(self, dlc):
		tile = dlc.getCurrentTextureTile()
		tileKey = tile.tmemAddr | (tile.bpp << 9) | (tile.colorFormat << 12) | (self.tmemWriteCount << 15) | (tile.stMode[0] << 27) | (tile.stMode[1] << 30)
		if tileKey in self.materialDict:
			return self.materialDict[tileKey]

		mtlEnc = DLMaterialEncapsulation(dlc)			

		startTexIndex = len(self.textures)
		mainTex = None
		
		texPrefix = self.name + "_"
		
		drawData = self.drawData
		if tile.isValid:
			sysMem = self.sysMem
			tileWidth, tileHeight = tile.stSize
			
			width, height = tile.stMask
			width = min(1 << width, tileWidth)
			height = 1 << height
			
			texBits = TILEIMG_BPP_SIZES[tile.bpp]
			rowSize = ((width * texBits) + 7) // 8
			rowSize = (rowSize + 7) & ~7
			texSize = rowSize * height

			palColorCount = 16 if texBits <= 4 else 256
			palSize = (palColorCount << 1) if tile.colorFormat == TILEIMG_COLORFMT_CI else 0
			palData = None

			texAddrs = []
			if drawData and drawData.baseTexAddr and drawData.basePalAddr:				
				#eye and mouth textures are linear, but the main texture data is pre-formatted for tmem
				if drawData.eyeTexAddrs[0] and drawData.eyeTexPos and tile.tmemAddr == drawData.eyeTexPos:
					texAddrs = drawData.eyeTexAddrs
					isLinear = True
				elif drawData.mouthTexAddrs[0] and drawData.mouthTexPos and tile.tmemAddr == drawData.mouthTexPos:
					texAddrs = drawData.mouthTexAddrs
					isLinear = True
				elif self.boyPalTex and drawData.clothTexPos and tile.tmemAddr == drawData.clothTexPos:
					basePalAddr, baseTexAddr = self.boyPalTex
					if palSize:
						palAddr = basePalAddr + ((drawData.entryIndex + 38) << 5)
						palData = sysMem[palAddr : palAddr + palSize]
					texAddrs = [baseTexAddr + ((drawData.entryIndex + 38) << 9)]
					isLinear = True
				else:
					texAddrs = [drawData.baseTexAddr + (tile.tmemAddr << 3)]
					isLinear = False
					
				if not palData and palSize:
					palData = sysMem[drawData.basePalAddr : drawData.basePalAddr + palSize]
			else:
				tmem = dlc.getTMem()
				if palSize:
					if self.palTMemValid:
						palOffset = 0x800 + (tile.palIndex << 7)
						palData = tmem[palOffset : palOffset + palSize]
					else:
						#stub since our data set didn't include a palette load
						palData = bytearray((
							0x00, 0x00, 0x00, 0xFF,
							0x10, 0x10, 0x10, 0xFF,
							0x20, 0x20, 0x20, 0xFF,
							0x30, 0x30, 0x30, 0xFF,
							0x40, 0x40, 0x40, 0xFF,
							0x50, 0x50, 0x50, 0xFF,
							0x60, 0x60, 0x60, 0xFF,
							0x70, 0x70, 0x70, 0xFF,
							0x80, 0x80, 0x80, 0xFF,
							0x90, 0x90, 0x90, 0xFF,
							0xA0, 0xA0, 0xA0, 0xFF,
							0xB0, 0xB0, 0xB0, 0xFF,
							0xC0, 0xC0, 0xC0, 0xFF,
							0xD0, 0xD0, 0xD0, 0xFF,
							0xE0, 0xE0, 0xE0, 0xFF,
							0xFF, 0xFF, 0xFF, 0xFF,
						))
						palData = noesis.swapEndianArray(rapi.imageEncodeRaw(palData, 16, 1, "a1b5g5r5"), 2)
				mainTMemAddr = MEM_SIZE - 0x1000
				texTMemOffset = tile.tmemAddr << 3
				sysMem[mainTMemAddr : mainTMemAddr + texSize] = tmem[texTMemOffset : texTMemOffset + texSize]
				texAddrs.append(mainTMemAddr)
				isLinear = True

			if len(texAddrs) > 0:
				for texAddr in texAddrs:
					if isLinear:
						texData = sysMem[texAddr : texAddr + texSize]
					else:
						texData = rapi.imageN64ReadTMEM(sysMem[texAddr : texAddr + texSize], width, height, texBits)

					rgba = rapi.imageN64DecodeRGBA32(texData, palData, width, height, tile.colorFormat, tile.bpp, 4)

					#if set to clamp with an explicit wrap mask, repeat the texture manually
					sWrap, tWrap = tile.stMode
					wrapWidth = tileWidth if sWrap & 2 else width
					wrapHeight = tileHeight if sWrap & 2 else height
					if width != wrapWidth or height != wrapHeight:
						wrapRgba = bytearray(wrapWidth * wrapHeight * 4)
						rapi.imageTileInto32(wrapRgba, wrapWidth, wrapHeight, rgba, width, height, sWrap & 1, tWrap & 1)
						rgba = wrapRgba
						width = wrapWidth
						height = wrapHeight
					frameIndex = len(self.textures) - startTexIndex
					frameName = "" if frameIndex == 0 else "_frame%02i"%frameIndex
					tex = NoeTexture(texPrefix + "texture_%08X"%tileKey + frameName, width, height, rgba, noesis.NOESISTEX_RGBA32)
					mtlEnc.setTextureWrapFlags(tex)
					self.textures.append(tex)
				mainTex = self.textures[startTexIndex]
				
		mtl = mtlEnc.generateMaterial()
		mtl.name = "material_%08X"%tileKey
		if mainTex:
			mtl.setTexture(mainTex.name)
			texCount = len(self.textures) - startTexIndex
			if texCount > 1:
				#just for fun, let's cycle them
				cycleTime = 250.0 #250ms
				mtl.setExpr_texidx("%i + mod(time * %f, %i)"%(startTexIndex, 1.0 / cycleTime, texCount))
		
		mtlTexPair = (mtl, mainTex)
		self.materialDict[tileKey] = mtlTexPair
		self.materials.append(mtl)
		
		return mtlTexPair

	def createModel(self, baseAnims):
		rapi.rpgReset()
		dlc = DisplayListContext(DL_UCODEMODE_UC5, 2)
		dlc.setUserData(self)
		dlc.setVertexReadCallback(afReadVerts)
		dlc.setDrawTrianglesCallback(afDrawTris)
		dlc.setMatrixReadCallback(afReadMat)
		dlc.setTMemReadCallback(afReadTMem)
		dlc.setDisplayListCallback(afDisplayList)
				
		noeBones = afNoeBonesFromJointList(self.joints)
		noeAnims = []
		if len(baseAnims) > 0 and noeBones:
			for baseAnim in baseAnims:
				noeAnim = baseAnim.createNoesisAnim(self.joints, self.name, noeBones)
				if noeAnim:
					if len(noeAnims) == 0 and noesis.optWasInvoked("-afskelanm"):
						for boneIndex in range(len(noeBones)):
							noeBones[boneIndex].setMatrix(noeAnim.frameMats[boneIndex])
						noeBones = rapi.multiplyBones(noeBones)		
						for boneIndex in range(len(noeBones)):
							self.joints[boneIndex].modelTransform = noeBones[boneIndex].getMatrix().toMat44()
					noeAnims.append(noeAnim)
				
		self.drawToBoneIndex = {}
		self.drawJoints = []
		for jointIndex in range(len(self.joints)):
			joint = self.joints[jointIndex]
			if joint.dlAddr:
				joint.drawIndex = len(self.drawJoints)
				self.drawToBoneIndex[joint.drawIndex] = jointIndex
				self.drawJoints.append(joint)
				
		if len(self.drawJoints) != self.displayJointCount:
			print("Warning: Expected draw transform count mismatch:", len(self.drawJoints), "vs", self.displayJointCount)
		
		self.currentDrawIndex = 0
		self.vertToDrawIndex = {}
		
		for joint in self.drawJoints:
			#not every displaylist pushes a matrix, so explicitly default to the matrix belonging to this joint as we begin new lists
			self.currentDrawIndex = joint.drawIndex
			self.currentNodeIndex = joint.jointIndex
			dlSize = dlc.calculateDisplayListSize(self.sysMem, joint.dlAddr)
			dlc.runCommands(self.sysMem[joint.dlAddr : joint.dlAddr + dlSize])
			
		if self.baseDrawAddr:
			self.currentDrawIndex = -1
			dlSize = dlc.calculateDisplayListSize(self.sysMem, self.baseDrawAddr)
			dlc.runCommands(self.sysMem[self.baseDrawAddr : self.baseDrawAddr + dlSize])
			#make sure tile is flushed
			tile = dlc.getCurrentTextureTile()
			if tile.isValid:
				self.getMaterialAndTextureForTile(dlc)

		rapi.rpgOptimize()
		if noesis.optWasInvoked("-afusecolors"):
			rapi.rpgSmoothNormals()
		try:
			mdl = rapi.rpgConstructModel()
		except:
			mdl = None
			
		modelMats = NoeModelMaterials(self.textures, self.materials)
		if mdl:
			if len(noeAnims) > 0:
				mdl.setAnims(noeAnims)
			mdl.setBones(noeBones)
			mdl.setModelMaterials(modelMats)
		elif len(self.textures) > 0:
			mdl = NoeModel([], [], [], modelMats)

		return mdl
		
class SkeletonEntry(AFModel):
	def __init__(self, name, data, drawData, sysMem, animScratchAddrs, boyPalTex):
		bs = NoeBitStream(data, NOE_BIGENDIAN)
		super().__init__(name, drawData, 0, sysMem, boyPalTex)
		self.animScratchAddrs = animScratchAddrs
		jointCount = bs.readUByte()
		self.displayJointCount = bs.readUByte()
		bs.readUShort() #pad
		jointTableAddr = bs.readUInt()
		if jointTableAddr:
			jointsData = sysMem[jointTableAddr : jointTableAddr + jointCount * JointEntry.DataSize]
			jointsBs = NoeBitStream(jointsData, NOE_BIGENDIAN)
			for jointIndex in range(jointCount):
				self.joints.append(JointEntry(jointIndex, jointsBs))

			#get parents set up and do hierarchical transform
			self.recurseIndex = 0
			while self.recurseIndex < jointCount:
				self.recurseChildJoints(-1, self.joints)
			for joint in self.joints:
				#for validation, should already be sorted by index
				#joint.childList = sorted(joint.childList, key=lambda a: a.jointIndex)
				joint.transform(self.joints)
		else:
			print("Error: No joint table pointer, must've missed it in the object fixup!")
			
	def recurseChildJoints(self, parentIndex, joints):
		jointIndex = self.recurseIndex
		self.recurseIndex += 1
		joint = joints[jointIndex]
		joint.parentIndex = parentIndex
		if parentIndex >= 0:
			joints[parentIndex].childList.append(joint)
		for childIndex in range(joint.childCount):
			self.recurseChildJoints(jointIndex, joints)

class AnimationEntry:
	DataSize = 64
	OldDataSize = 20
	def __init__(self, name, data, sysMem, oldVersion):
		bs = NoeBitStream(data, NOE_BIGENDIAN)
		self.name = name
		self.sysMem = sysMem
		self.oldVersion = oldVersion
		self.noeAnim = None
		self.keyFlagsAddr = bs.readUInt()
		self.dataAddr = bs.readUInt()
		self.keyCountTblAddr = bs.readUInt()
		self.keyConstAddr = bs.readUInt()
		self.texAnimindex = bs.readShort()
		self.frameCount = bs.readShort()
		if oldVersion:
			self.startTime = 0.0
			self.endTime = 0.0
		else:
			self.startTime = bs.readFloat()
			self.endEnd = bs.readFloat()
		#don't care about the rest for now
		
	KeyBit_RotationX = (1 << 0)
	KeyBit_RotationY = (1 << 1)
	KeyBit_RotationZ = (1 << 2)
	KeyBit_TranslationX = (1 << 3)
	KeyBit_TranslationY = (1 << 4)
	KeyBit_TranslationZ = (1 << 5)
	
	def loadLists(self, boneCount):
		if not self.keyFlagsAddr or not self.dataAddr or not self.keyCountTblAddr:
			return False

		self.boneCount = boneCount
		sysMem = self.sysMem
		self.keyFlags = sysMem[self.keyFlagsAddr : self.keyFlagsAddr + boneCount]
		usedChannelTotal = 0
		usedRotChannelTotal = 0
		usedRootChannelTotal = 0
		for boneIndex in range(boneCount):
			kf = self.keyFlags[boneIndex]
			allBits = kf & 63
			rotBits = kf & 7
			usedChannels = noesis.countBits(allBits)
			usedChannelTotal += usedChannels
			if self.oldVersion and boneIndex == 0:
				usedRootChannelTotal += usedChannels
			else:
				usedRotChannelTotal += noesis.countBits(rotBits)
			
		self.keyCountTbl = noeUnpack(">" + "h" * usedChannelTotal, sysMem[self.keyCountTblAddr : self.keyCountTblAddr + usedChannelTotal * 2])
		if self.oldVersion:
			unusedRotChannelTotal = (boneCount - 1) * 3 - usedRotChannelTotal
			unusedRotChannelTotal += 6 - usedRootChannelTotal
		else:
			unusedRotChannelTotal = boneCount * 3 - usedRotChannelTotal
		self.keyConst = noeUnpack(">" + "h" * unusedRotChannelTotal, sysMem[self.keyConstAddr : self.keyConstAddr + unusedRotChannelTotal * 2]) if self.keyConstAddr else []
		keyDataCount = sum(self.keyCountTbl) * 3
		self.keyData = noeUnpack(">" + "h" * keyDataCount, sysMem[self.dataAddr : self.dataAddr + keyDataCount * 2])

		return True
		
	def createNoesisAnim(self, joints, modelName, noeBones):
		if len(joints) != self.boneCount:
			return None
		#i dunno, i guess this looks right? semi-verified by checking ranges through a bunch of animations as seen below
		toAngle = (1.0 / 1800.0) * 180.0
		#print("max/min val:", max(self.keyData), min(self.keyData))
		#print("max/min const val:", max(self.keyConst), min(self.keyConst))
		mats = [NoeMat43() for x in range(self.boneCount * self.frameCount)]
		keyDataIndex = 0
		keyConstIndex = 0
		usedChannelIndex = 0
		rootKeyConstIndex = 0
		rootRotIsFirst = True
		rootTrnConstCount = 3 - noesis.countBits(self.keyFlags[0]) if rootRotIsFirst else 0
		
		jointMap = {}
		#right/left joints are swapped, but only on this guy.
		#could probably handle this properly by using base pose data that's only present for these old-style skeletons.
		if self.oldVersion and "cKF_bs_r_he2" in modelName:
			jointMap = {
				19 : 26, 20 : 27, 21 : 28, 22 : 29, 23 : 30, 24 : 31, 25 : 32,
				26 : 19, 27 : 20, 28 : 21, 29 : 22, 30 : 23, 31 : 24, 32 : 25
			}
		
		try:
			for boneIndex in range(self.boneCount):
				destBoneIndex = boneIndex if not boneIndex in jointMap else jointMap[boneIndex]
				joint = joints[destBoneIndex]
				kf = self.keyFlags[boneIndex]
				trn = [ [], [], [] ]
				rot = [ [], [], [] ]
				for t in range(6):
					isRot = t < 3
					kl = rot if isRot else trn
					klIndex = t if isRot else t - 3
					if kf & (1 << t):
						keyCount = self.keyCountTbl[usedChannelIndex]
						usedChannelIndex += 1
						for keyIndex in range(keyCount):
							time = float(self.keyData[keyDataIndex] - self.startTime)
							value = self.keyData[keyDataIndex + 1]
							slope = self.keyData[keyDataIndex + 2] #unused
							keyDataIndex += 3
							kl[klIndex].append((time, float(value)))
					else:
						useConst = (rootRotIsFirst and boneIndex == 0) or isRot
						if useConst:
							keyIndex = keyConstIndex
							if rootTrnConstCount and boneIndex == 0:
								if isRot:
									keyIndex += rootTrnConstCount
								else:
									keyIndex = rootKeyConstIndex
									rootKeyConstIndex += 1
							kl[klIndex].append((0.0, float(self.keyConst[keyIndex])))
							keyConstIndex += 1
						else: #translations don't draw from the constant table but rather the base joint
							kl[klIndex].append((0.0, float(joint.translation[klIndex])))

				rot[0] = noesis.lerpSamples(rot[0], self.frameCount)
				rot[1] = noesis.lerpSamples(rot[1], self.frameCount)
				rot[2] = noesis.lerpSamples(rot[2], self.frameCount)
				trn[0] = noesis.lerpSamples(trn[0], self.frameCount)
				trn[1] = noesis.lerpSamples(trn[1], self.frameCount)
				trn[2] = noesis.lerpSamples(trn[2], self.frameCount)
				
				for frameIndex in range(0, self.frameCount):
					mat = NoeMat43()
					if self.oldVersion:
						mat = NoeMat43()
						mat = mat.rotate(-rot[0][frameIndex] * toAngle, (0.0, 1.0, 0.0))
						mat = mat.rotate(-rot[1][frameIndex] * toAngle, (1.0, 0.0, 0.0))
						mat = mat.rotate(rot[2][frameIndex] * toAngle, (0.0, 0.0, 1.0))					
					else:
						mat = mat.rotate(rot[0][frameIndex] * toAngle, (1.0, 0.0, 0.0))
						mat = mat.rotate(-rot[1][frameIndex] * toAngle, (0.0, 1.0, 0.0))
						mat = mat.rotate(rot[2][frameIndex] * toAngle, (0.0, 0.0, 1.0))
					mat[3] = NoeVec3((trn[0][frameIndex], trn[1][frameIndex], trn[2][frameIndex]))
					mats[destBoneIndex + frameIndex * self.boneCount] = mat
					
			return NoeAnim(self.name, noeBones, self.frameCount, mats, DEFAULT_FRAMERATE)
		except:
			return None #assume it was meant for a different skeleton or something

def afCreateBaseAnim(animIndex, animAddrs, sysMem, addrToSizeName, boneCount):
	animAddr = animAddrs[animIndex]
	animSize, animName = addrToSizeName[animAddr]
	print("Loading base animation:", animName)
	oldVersion = (animSize == AnimationEntry.OldDataSize)
	anim = AnimationEntry(animName, sysMem[animAddr : animAddr + animSize], sysMem, oldVersion)
	if anim.loadLists(boneCount):
		return anim
	return None

def afCreateBaseAnims(animAddrs, sysMem, preferAnimIndex, addrToSizeName, boneCount):
	baseAnims = []
	if len(animAddrs) > 0:
		if LOAD_ALL_ANIMS:
			for animIndex in range(len(animAddrs)):
				anim = afCreateBaseAnim(animIndex, animAddrs, sysMem, addrToSizeName, boneCount)
				if anim:
					baseAnims.append(anim)
		else:
			animIndex = preferAnimIndex if len(animAddrs) > preferAnimIndex else 0
			anim = afCreateBaseAnim(animIndex, animAddrs, sysMem, addrToSizeName, boneCount)
			if anim:
				baseAnims.append(anim)

	if len(baseAnims) == 0:
		print("Warning: Failed to load base animation, skeleton transforms will be have no rotation.")
	return baseAnims

def afPrepDraw(skelName, sysMem, symDict, addrToSizeName):
	if OLD_NPC:
		#need to explicitly copy eye/mouth texture into the correct location
		charNameOffset = skelName.find(SKELETON_PREFIX)
		if charNameOffset >= 0:
			charName = skelName[charNameOffset + len(SKELETON_PREFIX):]
			if charName.startswith("r_"):
				charName = charName[2:]
				
			scratchNames = (("anime_1_txt", "eye", ), ("anime_2_txt", "kuchi"))				
			for scratchName, texSuffix in scratchNames:
				if scratchName in symDict:
					scratchAddr, scratchSize = symDict[scratchName]
					texName = charName + "_" + texSuffix + str(OLD_NPC_FACE_TEX_INDEX) + "_TA_txt"
					if texName in symDict:
						texAddr, texSize = symDict[texName]
						sysMem[scratchAddr : scratchAddr + texSize] = sysMem[texAddr : texAddr + texSize]
	
def afTextureSizeBestGuess(texData, bpp):
	texSize = len(texData)
	if FORCE_ADDITIONAL_TEXTURE_WIDTH:
		w = FORCE_ADDITIONAL_TEXTURE_WIDTH
	else:
		texelCount = ((texSize * bpp) + 7) // 8
		w = noesis.nextPow2(int(math.sqrt(texelCount) + 0.5))
	rowSize = ((w * bpp) + 7) // 8
	rowSize = (rowSize + 7) & ~7
	h = texSize // rowSize
	return w, h

def npcObjectLoadModelInternal(data, mdlList, nameList, selectedFile):
	ctx = rapi.rpgCreateContext()

	#0x00001 = big endian
	#0x00002 = large page alignment
	#0x10000 = relocation (incomplete, use at your own risk) enabled
	elfLoaderFlags = 0x00001 | 0x00002 | 0x10000
	elfHandle = rapi.elfLoaderInit(MEM_SIZE, elfLoaderFlags)

	sysMem = None
	try:
		if ONLY_LOAD_IMMEDIATE_OBJECT:
			rapi.elfLoaderLoadData(elfHandle, data)
		else:
			#just load everything under this directory instead
			scanDir = rapi.getDirForFilePath(selectedFile)
			for root, dirs, files in os.walk(scanDir):
				for localPath in files:
					if localPath.lower().endswith(".o"):
						fullPath = os.path.join(root, localPath)
						print("Loading object:", fullPath)
						rapi.elfLoaderLoadPath(elfHandle, fullPath)
		
		print("Linking objects and building symbol dictionary.")
		symCount = rapi.elfLoaderSymbolCount(elfHandle)
		symDict = {}
		addrToSizeName = {}
		animAddrs = []
		animScratchAddrs = []
		additionalSkeletons = set()
		additionalModels = set()
		additionalTextures = set()
		lskelPrefix = SKELETON_PREFIX.lower()
		for symIndex in range(symCount):
			name, addr, size, packInfo = rapi.elfLoaderSymbolInfo(elfHandle, symIndex)
			if name:
				symDict[name] = (addr, size)
				addrToSizeName[addr] = size, name
				lname = name.lower()
				if (size == AnimationEntry.DataSize or size == AnimationEntry.OldDataSize) and lname.startswith("ckf_ba_"):
					animAddrs.append(addr)
				elif lname.startswith("anime_model_"):
					animScratchAddrs.append(addr)
				elif lname.startswith(lskelPrefix):
					additionalSkeletons.add(addr)
				elif lname.endswith("_model"):
					additionalModels.add(addr)
				elif lname.endswith("_txt") or lname.endswith("_tex"):
					additionalTextures.add(addr)
			
		#when loading a matrix in a displaylist, we'll need to figure out which buffer the pointer is intended to be relative to
		animScratchAddrs = sorted(animScratchAddrs, key=lambda a: -a)
			
		#just read it all back in one go
		sysMem = rapi.elfLoaderReadMemory(elfHandle, 0, MEM_SIZE)
	except:
		print("Encountered an exception while loading object data.")
		
	rapi.elfLoaderFree(elfHandle)
	
	if sysMem:
		ctx = rapi.rpgCreateContext()
	
		triedToCreateBaseAnims = False
		baseAnims = []

		if noesis.optWasInvoked("-afobjanim"):
			preferAnimIndex = int(noesis.optGetArg("-afobjanim"))
		else:
			preferAnimIndex = 0
			searchAnim = "cKF_ba_r_npc_1_banzai1" if not OLD_NPC else "cKF_ba_r_oba_walk"
			for animIndex in range(len(animAddrs)):
				animAddr = animAddrs[animIndex]
				size, name = addrToSizeName[animAddr]
				if name == searchAnim:
					preferAnimIndex = animIndex
					break
		
		boyPalTex = None
		if "BOY_pallet_data" in symDict and "BOY_tex_data" in symDict:
			boyPalAddr, boyPalSize = symDict["BOY_pallet_data"]
			boyTexAddr, boyTexSize = symDict["BOY_tex_data"]
			boyPalTex = (boyPalAddr, boyTexAddr)
		else:
			print("Warning: No boy palette/texture data, some NPC palettes will be busted.")
		
		avoidDups = noesis.optWasInvoked("-afnodups")
		visitedSkels = set()
		
		hasDrawData = "npc_draw_data_tbl" in symDict
		if hasDrawData:
			tableOffset, tableSize = symDict["npc_draw_data_tbl"]
			drawEntrySize = DrawDataEntry.DataSize
			entryCount = tableSize // drawEntrySize
			for entryIndex in range(entryCount):
				entryOffset = tableOffset + entryIndex * drawEntrySize
				entry = DrawDataEntry(entryIndex, sysMem[entryOffset : entryOffset + drawEntrySize])
				if entry.skelAddr > 0 and entry.skelAddr in addrToSizeName:
					#remove the additional skeleton if it's being processed in the draw list
					if entry.skelAddr in additionalSkeletons:
						additionalSkeletons.remove(entry.skelAddr)

					skelSize, skelName = addrToSizeName[entry.skelAddr]
					if avoidDups:
						if skelName in visitedSkels:
							continue
						visitedSkels.add(skelName)
					
					afPrepDraw(skelName, sysMem, symDict, addrToSizeName)
					print("Loading:", skelName)
					skel = SkeletonEntry(skelName, sysMem[entry.skelAddr : entry.skelAddr + skelSize], entry, sysMem, animScratchAddrs, boyPalTex)
					if not triedToCreateBaseAnims:
						baseAnims = afCreateBaseAnims(animAddrs, sysMem, preferAnimIndex, addrToSizeName, len(skel.joints))
						triedToCreateBaseAnims = True
						
					#can't pre-generate the NoeAnim, as translations vary per model
					mdl = skel.createModel(baseAnims)
					if mdl:
						if nameList is not None:
							nameList.append(skelName)
						mdlList.append(mdl)

		#default to dumping additional models if we have no draw data
		if DUMP_ADDITIONAL_MODELS or not hasDrawData or len(mdlList) == 0:
			for skelAddr in additionalSkeletons:
				skelSize, skelName = addrToSizeName[skelAddr]
				if avoidDups:
					if skelName in visitedSkels:
						continue
					visitedSkels.add(skelName)
				afPrepDraw(skelName, sysMem, symDict, addrToSizeName)
				skelName = "no_draw_" + skelName
				print("Loading additional skeleton:", skelName)
				skel = SkeletonEntry(skelName, sysMem[skelAddr : skelAddr + skelSize], None, sysMem, animScratchAddrs, boyPalTex)
				if not triedToCreateBaseAnims:
					baseAnims = afCreateBaseAnims(animAddrs, sysMem, preferAnimIndex, addrToSizeName, len(skel.joints))
					triedToCreateBaseAnims = True
				mdl = skel.createModel(baseAnims)
				if mdl:
					if nameList is not None:
						nameList.append(skelName)
					mdlList.append(mdl)
					
			if len(mdlList) == 0:
				for mdlAddr in additionalModels:
					mdlSize, mdlName = addrToSizeName[mdlAddr]
					print("Loading additional model:", mdlName)
					afMdl = AFModel(mdlName, None, mdlAddr, sysMem, boyPalTex)
					mdl = afMdl.createModel([])
					if mdl:
						if nameList is not None:
							nameList.append(mdlName)
						mdlList.append(mdl)
						
				looseTextures = []
				for texAddr in additionalTextures:
					texSize, texName = addrToSizeName[texAddr]
					texSuffix = "_txt" if texName.lower().endswith("_txt") else "_tex"
					palName = texName.replace(texSuffix, "_pal")
					if palName not in symDict:
						#try another couple variants before giving up
						palName = texName.replace(texSuffix, "1_pal")
						if palName not in symDict:
							palName = texName.replace(texSuffix, "2_pal")
					if ADDITIONAL_TEXTURE_RGBA16:
						texData = noesis.swapEndianArray(sysMem[texAddr : texAddr + texSize], 2)
						w, h = afTextureSizeBestGuess(texData, 16)
						rgba = rapi.imageDecodeRaw(texData, w, h, "a1b5g5r5")					
						tex = NoeTexture(texName, w, h, rgba, noesis.NOESISTEX_RGBA32)
						looseTextures.append(tex)
					else:
						if palName in symDict:
							palAddr, palSize = symDict[palName]
							print("Loading additional texture:", texName)
							palData = noesis.swapEndianArray(sysMem[palAddr : palAddr + palSize], 2)
							texData = noesis.nybbleSwap(sysMem[texAddr : texAddr + texSize])
							w, h = afTextureSizeBestGuess(texData, 4)
							rgba = rapi.imageDecodeRawPal(texData, palData, w, h, 4, "a1b5g5r5")					
							tex = NoeTexture(texName, w, h, rgba, noesis.NOESISTEX_RGBA32)
							looseTextures.append(tex)
						else:
							print("Warning: Couldn't find palette for texture:", texName)
						
				if len(looseTextures) > 0:
					#create a model to house the loose textures
					modelMats = NoeModelMaterials(looseTextures, [])
					mdl = NoeModel([], [], [], modelMats)
					if nameList is not None:
						nameList.append("texture_holder")
					mdlList.append(mdl)

	if OLD_NPC:
		#put them in the same space as the newer ones
		rapi.parseInstanceOptions("-rotate 270 90 0")

	return 1
	
def npcObjectLoadModel(data, mdlList):
	return npcObjectLoadModelInternal(data, mdlList, None, rapi.getLastCheckedName())

def afMassDump(toolIndex):
	exportPath = noesis.userPrompt(noesis.NOEUSERVAL_FOLDERPATH, "Export Path", "Select an export destination directory.", os.path.join(noesis.getSelectedDirectory(), "npcdump"), None)
	if not exportPath:
		return 0	

	noesis.logPopup()
	
	noeMod = noesis.instantiateModule()
	noesis.setModuleRAPI(noeMod)
	
	mdlList = []
	nameList = []
	rapi.parseInstanceOptions(MASS_DUMP_IMPORT_OPTIONS)
	npcObjectLoadModelInternal(None, mdlList, nameList, noesis.getSelectedFile())
	#fix duplicate names
	uniqueNames = set()
	for nameIndex in range(len(nameList)):
		name = nameList[nameIndex]
		if name in uniqueNames:
			nameList[nameIndex] = name + "_entry%04i"%nameIndex
		else:
			uniqueNames.add(name)
	
	if len(mdlList) == 0:
		print("No objects or models were found on the path.")
	else:
		print("Generating native models.")
		rapi.toolSetGData(mdlList)
		loadedCount = rapi.toolGetLoadedModelCount()
		if loadedCount != len(mdlList):
			print("Error: There was a problem ingesting one or more models.", loadedCount, "vs", len(mdlList))
		else:
			os.makedirs(exportPath, exist_ok=True)
			for mdlIndex in range(loadedCount):
				exportName = os.path.join(exportPath, nameList[mdlIndex] + "." + MASS_DUMP_FORMAT)
				print("Writing", exportName)
				rapi.toolSetSelectedModelIndex(mdlIndex)
				rapi.toolExportGData(exportName, MASS_DUMP_EXPORT_OPTIONS)
		rapi.toolFreeGData()
		print("Finished writing", loadedCount, "models.")
	
	noesis.freeModule(noeMod)
	return 0
