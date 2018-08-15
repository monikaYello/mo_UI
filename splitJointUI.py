import pymel.core as pm
import mo_Utils.mo_riggUtils as mo_riggUtils
def splitSelJointUI():
	"""
	Script:     splitSelJointUI
	Descr:      Interface to rigg_tools.splitJnt
	Req:        rigg_tools.splitJnt
	"""
	
	segmentOpt=2

	win="splitSelJointWin"
	# Builds the interface for the splitSelJointUI
	if pm.window(win, exists=1):
		pm.deleteUI(win)
		
	pm.window(win, t="Split Selected Joints", w=100, h=100)
	f=pm.formLayout(nd=100)
	segments=pm.intSliderGrp(field=True, max=100, l="Segments", min=2)
	b1=pm.button(l="Okay")
	b2=pm.button(l="Cancel")
	pm.formLayout(f, 
		ap=[(b1, 'right', 0, 47), (b2, 'left', 0, 52)], 
		e=1, af=[(segments, 'top', 5), (segments, 'left', 5), (segments, 'right', 5), (b1, 'left', 5), (b1, 'bottom', 5), (b2, 'right', 5), (b2, 'bottom', 5)])
	# set up callbacks
	pm.button(b2, e=1, c=lambda *args: pm.deleteUI(win))
	pm.button(b1, e=1, c=lambda *args: mo_riggUtils.splitJnt(pm.intSliderGrp(segments, q=1, v=1)))
	# set up defaults
	
	# now set the item
	pm.intSliderGrp(segments, e=1, value=segmentOpt)
	pm.showWindow(win)
	
