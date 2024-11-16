from inc_noesis import *

def registerNoesisTypes():
	handle = noesis.registerTool("Load and preserve view", preserveViewToolMethod, "Load the selected file while preserving the current view.")
	noesis.setToolFlags(handle, noesis.NTOOLFLAG_CONTEXTITEM)
	return 1

def preserveViewToolMethod(toolIndex):
	if noesis.isPreviewModuleRAPIValid():
		noesis.setPreviewModuleRAPI()
		viewData = rapi.getInternalViewData()
	else:
		viewData = None
		
	noesis.openFile(noesis.getSelectedFile())
	
	if viewData and noesis.isPreviewModuleRAPIValid():
		noesis.setPreviewModuleRAPI() #the preview module was invalidated when we loaded a new scene, so set it again
		rapi.setInternalViewData(viewData)

	return 0
