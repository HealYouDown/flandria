from inc_noesis import *
from inc_atarijaguar import JagUtils

MAX_REASONABLE_FILE_SIZE = 1024 * 1024 * 8
MAX_REASONABLE_DECOMP_FILE_SIZE = 1024 * 1024 * 16

def registerNoesisTypes():
	handle = noesis.register("Atari Jaguar LZJ Archive", ".lzj")
	noesis.setHandlerExtractArc(handle, lzjExtractArc)
	return 1

def lzjExtractArc(fileName, fileLen, justChecking):
	if fileLen > MAX_REASONABLE_FILE_SIZE:
		return 0
		
	try:
		with open(fileName, "rb") as f:
			data = f.read()
			lzSize = JagUtils.lzjagDecompSize(data)
			if lzSize <= 0 or lzSize > MAX_REASONABLE_DECOMP_FILE_SIZE:
				return 0
				
			if not justChecking:
				decompData = JagUtils.lzjagDecomp(data, lzSize)
				name = "lzjag_decomp.bin"
				print("Writing", name)
				rapi.exportArchiveFile(name, decompData)				
			
			return 1
	except:
		pass
	return 0
