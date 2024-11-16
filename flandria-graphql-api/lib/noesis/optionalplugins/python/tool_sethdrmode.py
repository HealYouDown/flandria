from inc_noesis import *

def registerNoesisTypes():
	handle = noesis.registerTool("Enable HDR Mode", dvAdjustToolMethod, "Adjusts data viewer settings to enable HDR and post.")
	return 1
	
def dvAdjustToolMethod(toolIndex):
	if noesis.openDataViewer():
		noesis.setDataViewerSetting("HDR enabled", "1")
		noesis.setDataViewerSetting("Bloom enabled", "1")
		noesis.setDataViewerSetting("Bloom extra downsample", "2")
		noesis.setDataViewerSetting("HDR Env render", "1")
		noesis.setDataViewerSetting("HDR Env blur amount", "0.9")
		noesis.setDataViewerSetting("HDR Env intensity", "2.0")
		noesis.setDataViewerSetting("Material Env intensity", "1.75")
		noesis.setDataViewerSetting("Global Env power", "1.25")
		noesis.setDataViewerSetting("Render occlusion", "1")
		noesis.setDataViewerSetting("Render opacity mask", "1")
		noesis.setDataViewerSetting("Main HDR buffer MSAA", "4")
		noesis.closeDataViewer()
		noesis.messagePrompt("Settings have been applied. You'll need to restart Noesis for the changes to take effect.")
	return 0
	