from inc_noesis import *
from inc_atarijaguar import JagUtils

#default header produced by tga2cry doesn't have a distinction between cry and rgb (although it's implicit at >16bpp)
FORCE_RGB = False

def registerNoesisTypes():
	handle = noesis.register("Atari Jaguar CRY Image", ".cry")
	noesis.setHandlerTypeCheck(handle, cryCheckType)
	noesis.setHandlerLoadRGBA(handle, cryLoadRGBA)
	noesis.setHandlerWriteRGBA(handle, cryWriteRGBA)
	return 1

class CryImage:	
	def __init__(self, data, validateWidth = True):
		self.pixelSize = 0
		if len(data) > 8:
			width, height, flags = noeUnpack(">HHI", data[:8])
			phraseGap, pixelSize, zOffset, decWidth = JagUtils.decodeBlitterFlags(flags)
			#only consider it valid if the encoded width matches the explicit one
			if (not validateWidth) or (width == decWidth):
				if pixelSize <= 32:
					self.pixelDataSize = (width * height * pixelSize + 7) // 8
					if len(data) >= (8 + self.pixelDataSize):
						self.width = width
						self.height = height
						self.pixelSize = pixelSize
						self.data = data

	def isValid(self):
		return self.pixelSize > 0
		
	def decode16(self, offset, colorCount):
		dataSlice = self.data[offset : offset + colorCount * 2]
		if FORCE_RGB:
			data = noesis.swapEndianArray(dataSlice, 2)
			return rapi.imageDecodeRaw(data, len(data) // 2, 1, "p1g5b5r5")
		else:
			return JagUtils.cryToRgba32(dataSlice)
		
	def decode(self):
		rgba = None
		if self.pixelSize >= 24:
			data = self.data[8 : 8 + self.width * self.height * 4]
			rgba = rapi.imageDecodeRaw(data, len(data) // 4, 1, "g8r8p8b8")
		elif self.pixelSize >= 16:
			rgba = self.decode16(8, self.width * self.height)
		else:
			bs = NoeBitStream(self.data, NOE_BIGENDIAN)
			bs.setByteEndianForBits(NOE_BIGENDIAN)
			bs.seek(8, NOESEEK_ABS)
			palOffset = 8 + self.pixelDataSize
			rgbaSize = self.width * self.height * 4
			rgba = bytearray(rgbaSize)
			if palOffset < len(self.data):
				bs.pushOffset()
				bs.seek(palOffset, NOESEEK_ABS)
				colorCount = bs.readUShort()
				bs.popOffset()
				
				palRgba = self.decode16(palOffset + 2, colorCount)
				for offset in range(0, rgbaSize, 4):
					palEntryOffset = bs.readBits(self.pixelSize) * 4
					rgba[offset : offset + 4] = palRgba[palEntryOffset : palEntryOffset + 4]
			else:
				for offset in range(0, rgbaSize, 4):
					maskValue = bs.readBits(self.pixelSize)
					rgba[offset : offset + 4] = (maskValue, maskValue, maskValue, 255)
		
		return NoeTexture("jagcrytex", self.width, self.height, rgba, noesis.NOESISTEX_RGBA32) if rgba else None				
	
def cryCheckType(data):
	try:
		cry = CryImage(data)
		return 1 if cry.isValid() else 0
	except:
		return 0

def cryLoadRGBA(data, texList):
	cry = CryImage(data)
	tex = cry.decode()
	if tex:
		texList.append(tex)
	return 1

def cryWriteRGBA(data, width, height, bs):
	flags = JagUtils.closestTextureWidth(width)
	encWidth = JagUtils.decodeTextureWidth(flags)
	if encWidth != width:
		print("Warning: Unsupported width, resizing from", width, "to", encWidth)
		data = rapi.imageResample(data, width, height, encWidth, height)
	bs.setEndian(NOE_BIGENDIAN)
	bs.writeUShort(encWidth)
	bs.writeUShort(height)
	#write as 16bpp cry (assume 0-phrase gap)
	xAddInc = 0x30000
	pixel16 = (4 << 3)
	bs.writeUInt(flags | xAddInc | pixel16)
	bs.writeBytes(JagUtils.rgba32ToCry(data[:encWidth * height * 4]))
	return 1
