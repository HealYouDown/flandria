from inc_noesis import *
import json
import os
import math
import re

ENCODE_BC = False
ENCODE_BC_WITH_ALPHA = False
SPEC_AA_HEADER = "NOESIS_SPECULAR_AA_INPUT"

"""
An example file where we want to filter roughness in the green channel of test_mro.png, and use the mesh "GloveShape" from test.fbx to generate model space normals:

NOESIS_SPECULAR_AA_INPUT
{
	"normal" : "test_normal.png",
	"mro" : "test_mro.png",
	"roughnessChannelIndex" : 1,
	"prefilterType" : 0,
	"roughnessIsGloss" : 0,
	"roughnessScale" : 1.0,
	"normalIsGamma" : 0,
	"normalIsSigned" : 0,
	"mroIsGamma" : 0,
	"skipMips" : 0,
	"model" : "test.fbx",
	"meshFilter" : "^GloveShape$",
	"meshCull" : 0,
	"meshSort" : 1
}
"""

def registerNoesisTypes():
	handle = noesis.register("Specular AA Filter", ".specaa")
	noesis.setHandlerTypeCheck(handle, specFilterCheckType)
	noesis.setHandlerLoadRGBA(handle, specFilterLoadRGBA)	
	return 1

def specFilterCheckType(data):
	if len(data) <= len(SPEC_AA_HEADER):
		return 0
	return 1 if data[:len(SPEC_AA_HEADER)] == SPEC_AA_HEADER.encode("ASCII") else 0

def specFilterLoadRGBA(data, texList):	
	s = json.loads(noeStrFromBytes(data[len(SPEC_AA_HEADER):], "UTF-8"))
	mroLocal = s.get("mro")
	if not mroLocal:
		print("Error: No MRO path specified in file.")
		return 0		

	inputName = rapi.getLastCheckedName()
	basePath = rapi.getDirForFilePath(inputName)
	mroPath = os.path.join(basePath, mroLocal)
	
	normalLocal = s.get("normal")
	normalPath = os.path.join(basePath, normalLocal) if normalLocal else None
		
	srcTex = noesis.loadImageRGBA(mroPath)
	if not srcTex:
		print("Error: MRO texture not found at specified path:", mroPath)
		return 0				

	width = srcTex.width
	height = srcTex.height
	mipCount = int(math.log(max(width, height), 2)) + 1
	rgbaMRO = rapi.imageGetTexRGBA(srcTex)
	if s.get("mroIsGamma"):
		rgbaMRO = rapi.imageToLinear(rgbaMRO, width, height)
	
	if normalPath:
		normalTex = noesis.loadImageRGBA(normalPath)
		if not normalTex:
			print("Error: Normal texture not found at specified path:", normalPath)
			return 0				
		normalWidth = normalTex.width
		normalHeight = normalTex.height
		
		getTexRgbaFlags = noesis.TEXRGBAFLOAT_FLAG_RGB | noesis.TEXRGBAFLOAT_FLAG_NORMALIZE
		if not s.get("normalIsSigned"):
			getTexRgbaFlags |= noesis.TEXRGBAFLOAT_FLAG_SCALEANDBIAS
		if s.get("normalIsGamma"):
			getTexRgbaFlags |= noesis.TEXRGBAFLOAT_FLAG_TOLINEAR
		normals, normalsIsHDR = rapi.imageGetTexRGBAFloat(normalTex, getTexRgbaFlags)
	else:
		normalWidth = width
		normalHeight = height
		normals = None
	
	#if a model is specified, convert from tangent space to model space
	mdlLocal = s.get("model")
	if mdlLocal:
		mdlPath = os.path.join(basePath, mdlLocal)
		if os.path.exists(mdlPath):
			print("Generating model space normals from", mdlPath)
			noeMod = noesis.instantiateModule()
			noesis.storeCurrentRAPI()
			noesis.setModuleRAPI(noeMod)

			statusMsg = None
			
			try:
				rapi.toolLoadGData(mdlPath)
				mdlCount = rapi.toolGetLoadedModelCount()
				if mdlCount > 0:
					meshFilter = s.get("meshFilter")
					meshEx = re.compile(meshFilter) if meshFilter else None
					vertData = bytearray()
					for mdlIndex in range(mdlCount):
						mdl = rapi.toolGetLoadedModel(mdlIndex)
						for mesh in mdl.meshes:
							if not meshEx or meshEx.match(mesh.name):
								for index in mesh.indices:
									uv = mesh.uvs[index]
									tan = mesh.tangents[index]
									vertData += uv.toBytes() + tan[0].toBytes() + tan[1].toBytes() + tan[2].toBytes()
					if len(vertData) == 0:
						statusMsg = "Warning: Couldn't generate uv/tangent data from " + mdlPath + "/" + meshFilter
					else:
						transformFlags = s.get("meshCull", 0) | (s.get("meshSort", 0) << 2)					
						normals = rapi.imageTransformTangentSpaceNormals(normals, normalWidth, normalHeight, vertData, transformFlags)
						outputModelSpaceNormals = s.get("outputModelSpaceNormals")
						if outputModelSpaceNormals:
							quantizedNormalData = rapi.imagePackU8Normals(normals, normalWidth, normalHeight, 4)
							quantizedNormalPath = os.path.join(basePath, outputModelSpaceNormals)
							quantizedNormalTex = NoeTexture(quantizedNormalPath, normalWidth, normalHeight, quantizedNormalData, noesis.NOESISTEX_RGBA32)
							#include hdr data as well, in case the target format supports it
							quantizedNormalTex.setHDRData(rapi.scaleAndBiasPackedFloats(normals, 0.5, 0.5, 0.0, 1.0), noesis.kNHDRTF_RGB_F96, 0)
							quantizedNormalTex.flags |= noesis.NTEXFLAG_ISLINEAR | noesis.NTEXFLAG_HDRISLINEAR
							
							statusMsg = "Wrote model space normals to " + quantizedNormalPath
							noesis.saveImageFromTexture(quantizedNormalPath, quantizedNormalTex, s.get("outputModelSpaceNormalOptions"))
				else:
					statusMsg = "Warning: Failed to load any model data from " + mdlPath
			except:
				statusMsg = "Warning: Encountered an exception while processing model " + mdlPath
				
			noesis.freeModule(noeMod)
			noesis.restoreCurrentRAPI()
			if statusMsg:
				print(statusMsg)
		else:
			print(mdlPath, "is not a valid path")			
	
	if not normals:
		#failed to get any normals, but we still want to run through the rest of the path
		normals = noePack("fff", 0.0, 0.0, 1.0) * normalWidth * normalHeight
	
	roughChanIndex = s.get("roughnessChannelIndex", 1)
	roughnessScale = s.get("roughnessScale", 1.0)
	prefilterType = s.get("prefilterType", 0)
	prefilterFlags = 0
	if s.get("roughnessIsGloss"):
		prefilterFlags |= 1
	skipMips = s.get("skipMips", 0)
	
	bcEncodeFormat = noesis.FOURCC_BC3 if ENCODE_BC_WITH_ALPHA else noesis.FOURCC_BC1
	bcNoesisFormat = noesis.NOESISTEX_DXT5 if ENCODE_BC_WITH_ALPHA else noesis.NOESISTEX_DXT1
	
	dstData = bytearray()	
	minSize = 4 if ENCODE_BC else 1
	print("Resampling and filtering.")
	for mipIndex in range(mipCount):
		mipWidth = max(srcTex.width >> mipIndex, minSize)
		mipHeight = max(srcTex.height >> mipIndex, minSize)
		rgbaMRO = rapi.imageResampleBox(rgbaMRO, width, height, mipWidth, mipHeight)
		rgbaMip = rgbaMRO if mipIndex < skipMips else rapi.imagePrefilterRoughness(rgbaMRO, mipWidth, mipHeight, roughChanIndex, roughnessScale, normals, normalWidth, normalHeight, prefilterType, prefilterFlags)
		width = mipWidth
		height = mipHeight
		
		mipData = rapi.imageEncodeDXT(rgbaMip, 4, width, height, bcEncodeFormat) if ENCODE_BC else rgbaMip
		dstData += mipData
		
	newTex = NoeTexture(inputName, srcTex.width, srcTex.height, dstData, bcNoesisFormat if ENCODE_BC else noesis.NOESISTEX_RGBA32)
	newTex.setMipCount(mipCount)
	
	texList.append(newTex)
	return 1
