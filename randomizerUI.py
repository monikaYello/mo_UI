"""
import randomizerUI
"""

import pymel.core as pm

def randomizer_start():
	
	randomizer_deleteWindow()
	randomizer_createUserInterface()
	

def randomizer_deleteWindow():
	"""--------------------------------------------------------------------------
	Delete Window Procedure
	--------------------------------------------------------------------------"""
	

	if pm.window('randomizer_window', exists=1):
		print "// randomizer: restart. //\n"
		pm.deleteUI('randomizer_window', window=1)
		
	
	else:
		print "// randomizer: start. //\n"
		
	


def randomizer_createUserInterface():
	"""--------------------------------------------------------------------------
	Create User Interface Procedure
	--------------------------------------------------------------------------"""
	

	pm.window('randomizer_window', s=0, rtf=0, t="randomizer", wh=(300, 700))
	# Create UI elements
	pm.columnLayout('mainColumnLayout', h=790, w=248)
	pm.separator('selectedTransformObjectsSeparator', h=10, w=240, st="none")
	pm.text('selectedTransformObjectsText', fn="boldLabelFont", h=24, l="selected transform Objects", w=240, al="center")
	pm.textScrollList('selectedTransformObjectsTextScrollList', h=80, w=240)
	pm.button('loadObjectsButton', h=28, c=lambda *args: randomizer_loadSelection(0), l="load transform Objects", w=240)
	pm.separator('selectedMaterialsSeparator', h=10, w=240, st="none")
	pm.text('selectedMaterialsText', fn="boldLabelFont", h=24, l="selected Materials", w=240, al="center")
	pm.textScrollList('selectedMaterialsTextScrollList', h=80, w=240)
	pm.button('loadMaterialsButton', h=28, c=lambda *args: randomizer_loadSelection(1), l="load Materials", w=240)
	pm.separator('transformAttributesSeparator', h=10, w=240, st="none")
	pm.text('randomizeAttributesText', fn="boldLabelFont", h=24, l="randomize Attributes", w=240, al="center")
	pm.checkBoxGrp('randomizeAttributesCheckBoxGrp', h=24, l4="Material", l2="Rotate", l3="Scale", w=240, l1="Translate", ncb=4, cw=[(1, 67), (2, 57), (3, 50), (4, 57)])
	pm.separator('translateAttributesSeparator', h=10, w=240, st="none")
	pm.text('translateText', fn="boldLabelFont", h=24, l="Translate", w=240, al="center")
	pm.floatFieldGrp('minMaxXtranslateFloatFieldGrp', pre=3, el="max X", bgc=(0.25, 0, 0), h=24, l="min X", nf=2, v1=0, v2=0, w=240, cw=[(1, 60), (2, 60), (3, 60), (4, 60)])
	pm.floatFieldGrp('minMaxYtranslateFloatFieldGrp', pre=3, el="max Y", bgc=(0, 0.25, 0), h=24, l="min Y", nf=2, v1=0, v2=0, w=240, cw=[(1, 60), (2, 60), (3, 60), (4, 60)])
	pm.floatFieldGrp('minMaxZtranslateFloatFieldGrp', pre=3, el="max Z", bgc=(0, 0, 0.25), h=24, l="min Z", nf=2, v1=0, v2=0, w=240, cw=[(1, 60), (2, 60), (3, 60), (4, 60)])
	pm.separator('rotateAttributesSeparator', h=10, w=240, st="none")
	pm.text('rotateText', fn="boldLabelFont", h=24, l="Rotate", w=240, al="center")
	pm.floatFieldGrp('minMaxXrotateFloatFieldGrp', pre=3, el="max X", bgc=(0.25, 0, 0), h=24, l="min X", nf=2, v1=0, v2=0, w=240, cw=[(1, 60), (2, 60), (3, 60), (4, 60)])
	pm.floatFieldGrp('minMaxYrotateFloatFieldGrp', pre=3, el="max Y", bgc=(0, 0.25, 0), h=24, l="min Y", nf=2, v1=0, v2=0, w=240, cw=[(1, 60), (2, 60), (3, 60), (4, 60)])
	pm.floatFieldGrp('minMaxZrotateFloatFieldGrp', pre=3, el="max Z", bgc=(0, 0, 0.25), h=24, l="min Z", nf=2, v1=0, v2=0, w=240, cw=[(1, 60), (2, 60), (3, 60), (4, 60)])
	pm.separator('scaleAttributesSeparator', h=10, w=240, st="none")
	pm.text('scaleText', fn="boldLabelFont", h=24, l="Scale", w=240, al="center")
	pm.floatFieldGrp('minMaxXscaleFloatFieldGrp', pre=3, el="max X", bgc=(0.25, 0, 0), h=24, l="min X", nf=2, v1=1, v2=1, w=240, cw=[(1, 60), (2, 60), (3, 60), (4, 60)])
	pm.floatFieldGrp('minMaxYscaleFloatFieldGrp', pre=3, el="max Y", bgc=(0, 0.25, 0), h=24, l="min Y", nf=2, v1=1, v2=1, w=240, cw=[(1, 60), (2, 60), (3, 60), (4, 60)])
	pm.floatFieldGrp('minMaxZscaleFloatFieldGrp', pre=3, el="max Z", bgc=(0, 0, 0.25), h=24, l="min Z", nf=2, v1=1, v2=1, w=240, cw=[(1, 60), (2, 60), (3, 60), (4, 60)])
	pm.separator('randomizeSelectionSeparator', h=10, w=240, st="none")
	pm.button('randomizeAbsoluteButton', h=28, c=lambda *args: randomizer_randomizeSelection(), l="randomize Abolute", w=240)
	pm.button('randomizeRelativeButton', h=28, c=lambda *args: randomizer_randomizeSelection(relative=True), l="randomize Relative", w=240)
	pm.button('undoButton', h=28, c=lambda *args: pm.undo(), l="undo", w=240)
	pm.iconTextButton('staschiIconTextButton', h=28, c=lambda *args: randomizer_loadHelpWebsite(), l="www.staschi.com", w=240, st="textOnly")
	pm.setParent('..')
	pm.setParent('..')
	# Display UI
	pm.showWindow('randomizer_window')
	


def randomizer_loadSelection(_selectedType):
	"""--------------------------------------------------------------------------
	Load Selection Procedure
	--------------------------------------------------------------------------"""
	

	pm.melGlobals.initVar( 'int', '_selectedType' )
	pm.melGlobals['_selectedType'] = 0
	loadedTransformObjects=pm.ls(tr=1, sl=1)
	numberOfTransformObjects=len(loadedTransformObjects)
	loadedMaterial=pm.ls(mat=1, sl=1)
	numberOfMaterial=len(loadedMaterial)
	i=0
	if (not pm.melGlobals['_selectedType']) and (numberOfTransformObjects):
		pm.textScrollList('selectedTransformObjectsTextScrollList', e=1, ra=1)
		for i in range(i,numberOfTransformObjects):
			pm.textScrollList('selectedTransformObjectsTextScrollList', a=loadedTransformObjects[i], e=1)
			
		
	
	elif (not pm.melGlobals['_selectedType']) and (numberOfMaterial):
		pm.textScrollList('selectedMaterialsTextScrollList', e=1, ra=1)
		for i in range(i,numberOfMaterial):
			pm.textScrollList('selectedMaterialsTextScrollList', a=loadedMaterial[i], e=1)
			
		
	
	else:
		print "// randomizer: Not the right selection. List will not be updated. //\n"
		
	


def randomizer_randomizeSelection(relative=False):
	"""--------------------------------------------------------------------------
	randomize Selection Procedure
	--------------------------------------------------------------------------"""
	

	translateCheckbox=int(pm.checkBoxGrp('randomizeAttributesCheckBoxGrp', q=1, v1=1))
	rotateCheckbox=int(pm.checkBoxGrp('randomizeAttributesCheckBoxGrp', q=1, v2=1))
	scaleCheckbox=int(pm.checkBoxGrp('randomizeAttributesCheckBoxGrp', q=1, v3=1))
	materialCheckbox=int(pm.checkBoxGrp('randomizeAttributesCheckBoxGrp', q=1, v4=1))
	selectedTransformObjects=pm.textScrollList('selectedTransformObjectsTextScrollList', q=1, ai=1)
	selectedMaterials=pm.textScrollList('selectedMaterialsTextScrollList', q=1, ai=1)
	numberOfObjects=len(selectedTransformObjects)
	numberOfMaterial=len(selectedMaterials)
	minXtranslateRandomValue=float(pm.floatFieldGrp('minMaxXtranslateFloatFieldGrp', q=1, v1=1))
	maxXtranslateRandomValue=float(pm.floatFieldGrp('minMaxXtranslateFloatFieldGrp', q=1, v2=1))
	minYtranslateRandomValue=float(pm.floatFieldGrp('minMaxYtranslateFloatFieldGrp', q=1, v1=1))
	maxYtranslateRandomValue=float(pm.floatFieldGrp('minMaxYtranslateFloatFieldGrp', q=1, v2=1))
	minZtranslateRandomValue=float(pm.floatFieldGrp('minMaxZtranslateFloatFieldGrp', q=1, v1=1))
	maxZtranslateRandomValue=float(pm.floatFieldGrp('minMaxZtranslateFloatFieldGrp', q=1, v2=1))
	minXrotateRandomValue=float(pm.floatFieldGrp('minMaxXrotateFloatFieldGrp', q=1, v1=1))
	maxXrotateRandomValue=float(pm.floatFieldGrp('minMaxXrotateFloatFieldGrp', q=1, v2=1))
	minYrotateRandomValue=float(pm.floatFieldGrp('minMaxYrotateFloatFieldGrp', q=1, v1=1))
	maxYrotateRandomValue=float(pm.floatFieldGrp('minMaxYrotateFloatFieldGrp', q=1, v2=1))
	minZrotateRandomValue=float(pm.floatFieldGrp('minMaxZrotateFloatFieldGrp', q=1, v1=1))
	maxZrotateRandomValue=float(pm.floatFieldGrp('minMaxZrotateFloatFieldGrp', q=1, v2=1))
	minXscaleRandomValue=float(pm.floatFieldGrp('minMaxXscaleFloatFieldGrp', q=1, v1=1))
	maxXscaleRandomValue=float(pm.floatFieldGrp('minMaxXscaleFloatFieldGrp', q=1, v2=1))
	minYscaleRandomValue=float(pm.floatFieldGrp('minMaxYscaleFloatFieldGrp', q=1, v1=1))
	maxYscaleRandomValue=float(pm.floatFieldGrp('minMaxYscaleFloatFieldGrp', q=1, v2=1))
	minZscaleRandomValue=float(pm.floatFieldGrp('minMaxZscaleFloatFieldGrp', q=1, v1=1))
	maxZscaleRandomValue=float(pm.floatFieldGrp('minMaxZscaleFloatFieldGrp', q=1, v2=1))
	i=0
	defaultTranslate=pm.getAttr(selectedTransformObjects[i] + ".translate")
	defaultRotate=pm.getAttr(selectedTransformObjects[i] + ".rotate")
	defaultScale=pm.getAttr(selectedTransformObjects[i] + ".scale")

	if (relative==False):
		defaultTranslate=[0,0,0]
		defaultRotate=[0,0,0]
		defaultScale=[0,0,0]


	if (not translateCheckbox) and (not rotateCheckbox) and (not scaleCheckbox) and (not materialCheckbox):
		print "// randomizer: No randomize attribute selected. Please select the desired attribute and enter min / max values. //\n"
		
	
	else:
		for i in range(i,numberOfObjects):
			if translateCheckbox:
				randomTranslateX=float(pm.mel.rand(minXtranslateRandomValue, maxXtranslateRandomValue))
				randomTranslateY=float(pm.mel.rand(minYtranslateRandomValue, maxYtranslateRandomValue))
				randomTranslateZ=float(pm.mel.rand(minZtranslateRandomValue, maxZtranslateRandomValue))
				pm.setAttr((selectedTransformObjects[i] + ".translateX"), 
					randomTranslateX + defaultTranslate[0])
				pm.setAttr((selectedTransformObjects[i] + ".translateY"), 
					randomTranslateY + defaultTranslate[1])
				pm.setAttr((selectedTransformObjects[i] + ".translateZ"), 
					randomTranslateZ + defaultTranslate[2])
				
			if rotateCheckbox:
				randomRotateX=float(pm.mel.rand(minXrotateRandomValue, maxXrotateRandomValue))
				randomRotateY=float(pm.mel.rand(minYrotateRandomValue, maxYrotateRandomValue))
				randomRotateZ=float(pm.mel.rand(minZrotateRandomValue, maxZrotateRandomValue))
				pm.setAttr((selectedTransformObjects[i] + ".rotateX"), 
					randomRotateX + defaultRotate[0])
				pm.setAttr((selectedTransformObjects[i] + ".rotateY"), 
					randomRotateY + defaultRotate[1])
				pm.setAttr((selectedTransformObjects[i] + ".rotateZ"), 
					randomRotateZ + defaultRotate[2])
				
			if scaleCheckbox:
				randomScaleX=float(pm.mel.rand(minXscaleRandomValue, maxXscaleRandomValue))
				randomScaleY=float(pm.mel.rand(minYscaleRandomValue, maxYscaleRandomValue))
				randomScaleZ=float(pm.mel.rand(minZscaleRandomValue, maxZscaleRandomValue))
				pm.setAttr((selectedTransformObjects[i] + ".scaleX"), 
					randomScaleX + defaultScale[0])
				pm.setAttr((selectedTransformObjects[i] + ".scaleY"), 
					randomScaleY + defaultScale[1])
				pm.setAttr((selectedTransformObjects[i] + ".scaleZ"), 
					randomScaleZ + defaultScale[2])
				
			if materialCheckbox:
				randomMaterialFloat=float(pm.mel.rand(0, numberOfMaterial - 1))
				randomMaterialInt=int(pm.mel.floor(randomMaterialFloat + 0.5))
				pm.select(selectedTransformObjects[i], r=1)
				pm.hyperShade(assign=selectedMaterials[randomMaterialInt])
				pm.select(cl=1)
				
			
		
	selectedTransformObjects = []
	


def randomizer_loadHelpWebsite():
	"""/ --------------------------------------------------------------------------
	 Load Help Website Procedure
	 --------------------------------------------------------------------------"""
	

	pm.showHelp("http://www.staschi.com/script/randomizer/", absolute=1)
	print "// randomizer: help website loaded. //\n"
	


# --------------------------------------------------------------------------
# Calling Start Procedure
# -------------------------------------------------------
