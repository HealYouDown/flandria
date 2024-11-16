from inc_noesis import *

MAX_REASONABLE_FILE_SIZE = 1024 * 1024 * 16
MAX_REASONABLE_DECOMP_FILE_SIZE = 1024 * 1024 * 16
ENABLE_TOOLS = True

SA_DECOMP_SIZE_MASK = 0xFFFFFF00

def registerNoesisTypes():
	handle = noesis.register("Sega Channel SA Image", ".sa")
	noesis.setHandlerExtractArc(handle, saExtractArc)

	if ENABLE_TOOLS:
		handle = noesis.registerTool("Compress as SA", lambda u: saToolMethod(True), "Compresses file as SA image.")
		noesis.setToolSubMenuName(handle, "Sega Channel")
		noesis.setToolFlags(handle, noesis.NTOOLFLAG_CONTEXTITEM)
		handle = noesis.registerTool("Decompress as SA", lambda u: saToolMethod(False), "Decompresses file as SA image.")
		noesis.setToolSubMenuName(handle, "Sega Channel")
		noesis.setToolFlags(handle, noesis.NTOOLFLAG_CONTEXTITEM)
	
	return 1

def saFilterData(data):
	if len(data) <= 6:
		return data
	
	#this header also contains the decompressed size of the image and some other data, but we don't need it to decompress the image
	headerSize, srcSize = noeUnpack(">HI", data[:6])
	if headerSize > 0 and srcSize > 0 and (srcSize + headerSize) == len(data):
		return data[headerSize:]
	return data
	
def saToolMethod(doCompress):
	noesis.logPopup()

	srcName = noesis.getSelectedFile()
	if not srcName or os.path.exists(srcName) is not True:
		print("Selected file isn't readable through the standard filesystem.")
		return 0

	noeMod = noesis.instantiateModule()
	noesis.setModuleRAPI(noeMod)

	with open(srcName, "rb") as f:
		data = saFilterData(f.read())
	
	if doCompress:
		decompData = rapi.compressSegaChanSA(data)
	else:
		decompSize = rapi.getSegaChanSASize(data)
		if decompSize <= 0:
			print("Invalid compressed data stream.")
			decompData = None
		else:
			decompData = rapi.decompSegaChanSA(data, decompSize)[:decompSize & SA_DECOMP_SIZE_MASK]

	if decompData is not None:
		suffix = "_compressed" if doCompress else "_decompressed"
		savePath = os.path.splitext(srcName)[0] + suffix + ".bin"
		if os.path.exists(savePath):
			print("Couldn't write to path, file already exists:", savePath)
		else:
			with open(savePath, "wb") as fw:
				fw.write(decompData)		
			print("Successfully wrote", savePath)
		
	noesis.freeModule(noeMod)

	return 0
	
def saExtractArc(fileName, fileLen, justChecking):
	if fileLen > MAX_REASONABLE_FILE_SIZE:
		return 0
		
	try:
		with open(fileName, "rb") as f:
			data = saFilterData(f.read())
			lzSize = rapi.getSegaChanSASize(data)
			if lzSize <= 0 or lzSize > MAX_REASONABLE_DECOMP_FILE_SIZE:
				return 0
				
			if not justChecking:
				decompData = rapi.decompSegaChanSA(data, lzSize)[:lzSize & SA_DECOMP_SIZE_MASK]
				name = "segachan_sa_decomp.bin"
				print("Writing", name)
				rapi.exportArchiveFile(name, decompData)				
			
			return 1
	except:
		pass
	return 0
