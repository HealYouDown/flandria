from inc_noesis import *
import os

def registerNoesisTypes():
	handle = noesis.registerVrMenuItem("Browse models", browseMethod)
	return 1

SPECIAL_ITEM_COUNT = 2
	
class BrowseItem:
	def __init__(self, name, fullPath, isDir):
		self.isDir = isDir
		dirPrefix = "(dir) " if self.isDir else ""
		self.name = dirPrefix + name
		self.fullPath = fullPath

browseItems = []
browsePath = ""
browseLoadedFilePath = ""

def scanDirectory(scanDir):
	global browsePath
	browsePath = scanDir
	dirItems = []
	items = []
	for root, dirs, files in os.walk(scanDir):
		for localPath in dirs:
			fullPath = os.path.join(root, localPath)
			dirItems.append(BrowseItem(localPath, fullPath, True))
		for localPath in files:
			if noesis.isSupportedFileExtension(localPath):
				fullPath = os.path.join(root, localPath)
				items.append(BrowseItem(localPath, fullPath, False))
		break
	dirItems = sorted(dirItems, key=lambda a: a.name.lower())
	items = sorted(items, key=lambda a: a.name.lower())
	
	selIndex = 0
	if len(browseLoadedFilePath) > 0:
		for itemIndex in range(len(items)):
			if items[itemIndex].fullPath == browseLoadedFilePath:
				selIndex = SPECIAL_ITEM_COUNT + len(dirItems) + itemIndex
				break
				
	noesis.setCustomVrMenuItem(selIndex)
	
	return dirItems + items
	
def browseGetCount():
	return SPECIAL_ITEM_COUNT + len(browseItems)

def browseEnterCustomMenu():
	noesis.enterCustomVrMenuState(browseGetCount, browseGetName, browseSelected)
	
def browseSelected(menuItemIndex):
	global browseItems
	if menuItemIndex == 0:
		noesis.enterCustomVrMenuState(None, None, None)
	elif menuItemIndex == 1:
		parentDir = os.path.abspath(os.path.join(browsePath, os.pardir))
		if os.path.exists(parentDir):
			browseItems = scanDirectory(parentDir)
	else:
		item = browseItems[menuItemIndex - SPECIAL_ITEM_COUNT]
		if item.isDir:
			browseItems = scanDirectory(item.fullPath)
		else:
			noesis.enterCustomVrMenuState(None, None, None)
			global browseLoadedFilePath
			browseLoadedFilePath = item.fullPath
			noesis.openFile(item.fullPath)
		

def browseGetName(menuItemIndex):
	return "Cancel" if menuItemIndex == 0 else ".." + " (current path: " + browsePath + ")" if menuItemIndex == 1 else browseItems[menuItemIndex - SPECIAL_ITEM_COUNT].name
	
def browseMethod(menuItemIndex):
	global browseItems
	browseItems = []
	
	if len(browsePath) > 0:
		scanDir = browsePath
	else:
		scanDir = noesis.getSelectedDirectory()
		if not os.path.exists(scanDir):
			scanDir = noesis.getScenesPath()
	
	browseEnterCustomMenu()
	browseItems = scanDirectory(scanDir)
