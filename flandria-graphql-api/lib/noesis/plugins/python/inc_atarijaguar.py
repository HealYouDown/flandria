from inc_noesis import *

class JagUtils:
	RomBase = 0x800000
	DefaultBootCodeSize = 0x290 #includes some slop, the decrypt function doesn't care if there's a bit of excess

	#decodes using the table ripped straight from the SDK's ARTWORK.EXE (also referenced on page 28 of the Jaguar Software Reference Manual)
	def cryToRgba32(data, flags = 0):
		return rapi.imageJaguarCRYToRGBA(data, flags)
	#calculates intensity for each rgb and attempts to best-fit the x/y index to the reference table with no prior quantization.
	#generally produces a better psnr than the suggested implementation in the manual.
	def rgba32ToCry(data, flags = 0):
		return rapi.imageJaguarRGBAToCRY(data, flags)

	#returns the closest (without going under) supported texture width
	def closestTextureWidth(width):
		return rapi.imageJaguarClosestWidth(width)
	def decodeTextureWidth(flags):
		return rapi.imageJaguarDecodeWidth(flags)
	def decodeBlitterFlags(flags):
		phraseGap = flags & 3
		depth = 1 << ((flags >> 3) & 7)
		zOffset = (flags >> 6) & 7
		width = JagUtils.decodeTextureWidth(flags)
		return phraseGap, depth, zOffset, width
	def decodeBlitterAddMode(flags):
		xAddMode = (flags >> 16) & 3
		yAddMode = (flags >> 18) & 1
		xAddSign = (flags >> 19) & 1
		yAddSign = (flags >> 20) & 1
		return xAddMode, yAddMode, xAddSign, yAddSign
		
	#optional INDEX_BIT_COUNT, LENGTH_BIT_COUNT, and BREAK_EVEN can be fed to the decomp functions as additional arguments, but we assume defaults
	def lzjagDecomp(data, decompSize):
		return rapi.decompLZJag(data, decompSize)
	def lzjagDecompSize(data):
		return rapi.getLZJagSize(data)

	#optional key, chunk size and count parameters can be provided as additional arguments.
	#by default, the key from the bios is used with a chunk size of 65 and a count taken from the first byte of data.
	def decryptBootCode(data):
		return rapi.callExtensionMethod("jaguar_boot_decrypt", data)
	#assumes a factory stock code image. this will provide garbage for a rom with a custom header, such as one designed to just immediately write
	#$03D0DEAD to the start of gpu ram in order to bypass the bios security check.
	def bootCodeChecksum(data, doDecrypt = True):
		if doDecrypt:
			data = JagUtils.decryptBootCode(data)
			data = rapi.callExtensionMethod("jaguar_boot_fixup", data) #arrange the key as we'd expect decrypted code at $F035AC to do
		return data[0x34 : 0x34 + 0x10] #normally lives at $F035E0
