from inc_noesis import *

def registerNoesisTypes():
	handle = noesis.register("PKM Image", ".pkm")
	noesis.setHandlerTypeCheck(handle, pkmCheckType)
	noesis.setHandlerLoadRGBA(handle, pkmLoadRGBA)
	noesis.setHandlerWriteRGBA(handle, pkmWriteRGBA)
	noesis.addOption(handle, "-pkmetc2", "force etc2 encoding.", 0)
	return 1
	
class PKMImage:
	def __init__(self, reader):
		self.reader = reader

	def parseImageInfo(self):
		bs = self.reader
		if bs.getSize() < 16:
			return -1
		bs.seek(0, NOESEEK_ABS)
		magic = bs.readUInt()
		if magic != 0x504B4D20:
			return -1
		ver = bs.readUShort()
		if ver != 0x3230 and ver != 0x3130:
			return -1
		self.format = bs.readUShort()
		formatToString = (
			"rgb1",
			"rgb",
			"rgba",
			"rgba",
			"rgba1",
			"r",
			"rg",
			"rs",
			"rgs",
			"srgb",
			"srgba",
			"srgba1"
		)
		if self.format < 0 or self.format >= len(formatToString):
			return -1
		self.formatString = formatToString[self.format]
		self.alignedWidth = bs.readUShort()
		self.alignedHeight = bs.readUShort()
		self.width = bs.readUShort()
		self.height = bs.readUShort()
		self.dataOffset = bs.tell()
		return 0
		
	def decode(self):
		bs = self.reader
		remainingBuffer = bs.getBuffer()[self.dataOffset:]
		data = rapi.imageDecodeETC(remainingBuffer, self.width, self.height, self.formatString)
		return data
	
def pkmCheckType(data):
	pkm = PKMImage(NoeBitStream(data, NOE_BIGENDIAN))
	if pkm.parseImageInfo() != 0:
		return 0
	return 1

def pkmLoadRGBA(data, texList):
	pkm = PKMImage(NoeBitStream(data, NOE_BIGENDIAN))
	if pkm.parseImageInfo() != 0:
		return 0
	texList.append(NoeTexture("pkmtex", pkm.width, pkm.height, pkm.decode(), noesis.NOESISTEX_RGBA32))
	return 1

def pkmWriteRGBA(data, width, height, bs):
	hasAlpha = not rapi.imageOpaqueAlphaRGBA32(data)
	writeETC2 = hasAlpha or noesis.optWasInvoked("-pkmetc2")
	bs.setEndian(NOE_BIGENDIAN)
	bs.writeUInt(0x504B4D20)
	bs.writeUShort(0x3230 if writeETC2 else 0x3130)
	etcFormat = 3 if hasAlpha else 1 if writeETC2 else 0
	bs.writeUShort(etcFormat)
	alignedWidth = (width + 3) & ~3
	alignedHeight = (height + 3) & ~3
	bs.writeUShort(alignedWidth)
	bs.writeUShort(alignedHeight)
	bs.writeUShort(width)
	bs.writeUShort(height)
	encodingQuality = 3 #use 1 for fast, 10 for exhaustive, but be warned, i didn't bother threading this thing out and ETCPACK is terrible
	print("Encoding image as ETC" + ("2" if writeETC2 else "1") + " at quality", encodingQuality)
	#if you want PICA200-style ETC encoding, use data = rapi.imageTilePICA200ETC(rapi.swapEndianArray(data, 8), w, h, 8), where data is the output of rapi.imageEncodeETC with format 0.
	#if you want ETC1-A4, do the same thing, but feed a block size of 16 to imageTilePICA200ETC and interleave your 4-bit alphas before calling it.
	#the "A4" isn't actually block compressed; it's just a 4x4 chunk of quantized 4-bit values, so you can use a bit transform or whatever you please and slap it on the front of each ETC block.
	bs.writeBytes(rapi.imageEncodeETC(data, width, height, etcFormat, encodingQuality))
	return 1
