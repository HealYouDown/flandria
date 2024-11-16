from inc_noesis import *

#this palette won't be a match for most of the images, but it's good enough to get an idea of what the thing is
DEFAULT_PALETTE = "GENERIC.PAL"

def registerNoesisTypes():
	handle = noesis.register("Power Up Baseball Image", ".img")
	noesis.setHandlerTypeCheck(handle, pbbImgCheckType)
	noesis.setHandlerLoadRGBA(handle, pbbImgLoadRGBA)
	return 1

def pbbImgDecompress(data, flag):
	if not (flag & 1):
		return data
	#simple rle implemented in asic
	bs = NoeBitStream(data)
	wbs = NoeBitStream()
	decompData = bytearray()
	while bs.tell() < len(data):
		c = bs.readUByte()
		if c & 0x80:
			c &= 0x7F
			for x in range(c):
				wbs.writeUByte(bs.readUByte())
		else:
			v = bs.readUByte()
			for x in range(c):
				wbs.writeUByte(v)			
	return wbs.getBuffer()

def pbbImgCheckType(data):
	if len(data) <= 5 or len(data) > 1024 * 1024:
		return 0
	width, height, flag = noeUnpack(">HHB", data[:5])
	data = pbbImgDecompress(data[5:], flag)
	if len(data) != width * height:
		return 0
	return 1

def pbbImgReadPal(path):
	if os.path.exists(path):
		palData = bytearray()
		with open(path, "r") as f:
			for line in f:
				db = line.find("dc.b")
				if db >= 0:
					toks = line[db + 4:].replace("	", "").replace(" ", "").split(",")
					for tok in toks:
						palByte = int(tok[1:], 16) if tok.startswith("$") else int(tok)
						palData += noePack("B", palByte)
		return palData
		
	#make a default palette
	return noePack("B" * 768, *[i // 3 for i in range(768)])

def pbbImgLoadRGBA(data, texList):
	defaultPalPath = os.path.abspath(rapi.getDirForFilePath(rapi.getLastCheckedName()) + "\\..\\PALETTES\\" + DEFAULT_PALETTE)
	palData = pbbImgReadPal(defaultPalPath)
	palData = rapi.imageDecodeRaw(palData, len(palData) // 3, 1, "r8g8b8") #expand to rgba
	palData[1023] = 0 #clear alpha for last entry
	
	width, height, flag = noeUnpack(">HHB", data[:5])
	data = pbbImgDecompress(data[5:], flag)
	pix = rapi.imageDecodeRawPal(data, palData, width, height, 8, "r8g8b8a8")
	texList.append(NoeTexture("pbbimg", width, height, pix, noesis.NOESISTEX_RGBA32))
	return 1
