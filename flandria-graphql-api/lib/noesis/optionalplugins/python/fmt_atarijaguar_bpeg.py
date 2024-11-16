from inc_noesis import *

REGISTER_DUMPER = True
#version 1 seems pretty broadly compatible with everything that used BPEG in the retail library, but if something looks busted you can try version 0
#(or possibly 2+ if i found more distinct variations to implement and didn't bother coming back to update this comment)
BPEG_VERSION = 1
BPEG_HEADER_WITH_QUANT_TABLES = 136

def registerNoesisTypes():
	handle = noesis.register("Atari Jaguar BPEG Image", ".bpeg")
	noesis.setHandlerTypeCheck(handle, bpegCheckType)
	noesis.setHandlerLoadRGBA(handle, bpegLoadRGBA)
	if REGISTER_DUMPER:
		handle = noesis.registerTool("Jaguar BPEG Dumper", bpegDumpToolMethod, "Dump BPEG files from a ROM image.")
		noesis.setToolFlags(handle, noesis.NTOOLFLAG_CONTEXTITEM)
		noesis.setToolVisibleCallback(handle, bpegDumpContextVisible)
	
	return 1
	
def bpegCheckType(data):
	if len(data) <= BPEG_HEADER_WITH_QUANT_TABLES:
		return 0
	id, w, h = noeUnpack(">IHH", data[:8])
	return 0 if id != 0x42504547 or w == 0 or h == 0 or w >= 4096 or h >= 4096 else 1

def bpegLoadRGBA(data, texList):
	tex = rapi.imageJaguarDecodeBPEG(data, BPEG_VERSION)
	if tex:
		texList.append(tex)
		return 1
	return 0

def bpegDumpContextVisible(toolIndex, selectedFile):
	if not selectedFile:
		return 0
	nameNoExt, ext = os.path.splitext(selectedFile)
	ext = ext.lower()
	if ext != ".j64":
		return 0
	return 1

def bpegDumpToolMethod(toolIndex):
	noesis.logPopup()

	noeMod = noesis.instantiateModule()
	noesis.setModuleRAPI(noeMod)
	
	romName = noesis.getSelectedFile()
	with open(noesis.getSelectedFile(), "rb") as f:
		data = f.read()
		offset = 0
		while offset >= 0:
			offset = data.find(b"BPEG", offset)
			if offset >= 0:
				bpegSize = rapi.imageJaguarGetBPEGSize(data[offset:], BPEG_VERSION)
				if bpegSize > 0:
					bpegName = rapi.getExtensionlessName(romName) + "_%08X.bpeg"%(offset)
					print("Writing", bpegName)
					with open(bpegName, "wb") as fw:
						fw.write(data[offset : offset + bpegSize])
					offset += BPEG_HEADER_WITH_QUANT_TABLES
				else:
					print("Skipping BPEG tag at %08X, doesn't look like valid BPEG data."%(offset))
					offset += 1

	noesis.freeModule(noeMod)
	return 0
