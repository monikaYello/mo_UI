import pymel.core as pm
import sys
import os
import maya.cmds as cmds
from functools import partial
myScriptPath = 'D:/Google Drive/PythonScripting/scripts'
if (not myScriptPath in sys.path):
    sys.path.insert(0,myScriptPath)
import mo_Utils.mo_alignUtils as mo_alignUtils
import mo_Utils.mo_displayUtils as mo_displayUtil
import mo_Utils.mo_riggUtils as mo_riggUtils
import mo_Utils.mo_stringUtils as mo_stringUtils
import mo_Utils.mo_animUtils as mo_animUtils
import mo_Utils.mo_meshUtils as mo_meshUtils
import mo_Utils.mo_shaderUtils as mo_shaderUtils
import mo_Utils.mo_fileSystemUtils as mo_fileSystemUtils
import mo_Tools.mog_ikFkSwitch.mog_ikFkSwitch as mog_ikFkSwitch
import mo_Tools.keyRandomizerUI as keyRandomizerUI
import mo_Tools.mo_storePoseToShelf as mo_storePoseToShelf
import mo_Tools.straightMotion as straightMotion
import mo_Tools.mo_imageplaneManager.mo_imageplaneManager as mo_imageplaneManager
#import mo_UI.splitJointUI as splitJointUI
import mo_Tools.mo_lightRigg as mo_lightRigg
import mo_Utils.libUtil as libUtil
import mo_Utils.mo_tempExport as tempExport
reload(mo_meshUtils)
reload(mo_fileSystemUtils)

tempExportDir = 'G:\\temp'

class mo_UI:
    def __init__(self):
        #Store UI elements in a dictionary
        self.UIElements = {}

        if pm.window("mo_UI_window", exists=True):
            pm.deleteUI("mo_UI_window")
        self.windowWidth = 400
        self.windowHeight = 598

        self.UIElements["window"] = pm.window("mo_UI_window", width=self.windowWidth, height=self.windowHeight, title="mo_UI_window")

        self.UIElements["topLevelColumn"] = pm.columnLayout(adjustableColumn=True, columnAlign="center")

        #Setup Tabs #every child creates new tab
        tabHeight = 500
        tabWidth = 400
        self.scrollWidth = tabWidth - 40

        self.UIElements["tabs"] = pm.tabLayout(height=tabHeight, innerMarginWidth=5, innerMarginHeight=5)

        riggTab = self.initializeRiggTab(tabHeight, tabWidth)
        pm.setParent("..")
        animTab = self.initializeAnimTab(tabHeight, tabWidth)
        pm.setParent("..")
        displayTab = self.initializeDisplayTab(tabHeight, tabWidth)
        pm.setParent("..")
        modelTab = self.initializeModelTab(tabHeight, tabWidth)
        pm.tabLayout(self.UIElements["tabs"], edit=True, tabLabel=((riggTab, 'mo_rigg'), (animTab, 'mo_anim'), (displayTab, 'mo_display'), (modelTab, 'mo_model')))

        #Display window
        pm.showWindow(self.UIElements["window"])



    '''def createScriptJob(self):
        self.jobNum = cmds.scriptJob(event=["SelectionChanged", self.modifySelected], runOnce=True, parent=self.UIElements["window"])
    
    def deleteScriptJob(self):
        cmds.scriptJob(kill=self.jobNum)'''

    def initializeRiggTab(self, tabHeight, tabWidth):
        columnWidth = 100
        moduleSpecific_scrollHeight = 120
        scrollHeight = tabHeight - moduleSpecific_scrollHeight - 20

        #1. Get Info
        self.UIElements["mainColumn"] = pm.columnLayout("mainColumn")

        pm.rowColumnLayout("snapRowColumn", numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])
        pm.button(label="snapT", parent="snapRowColumn", command=lambda a:mo_riggUtils.snap(pm.selected()[0], pm.selected()[-1], 'point'))
        pm.button(label="snapR", parent="snapRowColumn", command=lambda a:mo_riggUtils.snap(pm.selected()[0], pm.selected()[-1], 'orient'))
        pm.button(label="snap", parent="snapRowColumn", command=lambda a:mo_riggUtils.snap(pm.selected()[0], pm.selected()[-1]))

        pm.button(label="tempExport", parent="snapRowColumn", command=lambda a:mo_fileSystemUtils.tempExportSelected(path = tempExportDir))
        pm.button(label="tempImport", parent="snapRowColumn", command=lambda a:mo_fileSystemUtils.tempImport(path = tempExportDir))
        pm.button(label="tempExportUI", parent="snapRowColumn", command=lambda a:mo_fileSystemUtils.tempExportSelected(path = tempExportDir))
        
        pm.setParent(self.UIElements["mainColumn"])
        pm.separator()
        self.UIElements["3"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])

        pm.button(label="getTransforms", command=lambda a:mo_riggUtils.getTransformations())
        pm.button(label="getSkinInfluenceJoints", command=lambda a:mo_riggUtils.getSkinInfluenceJoints())
        pm.button(label="getJointChain", command=lambda a:mo_riggUtils.getJointChain())

        pm.button(label="getSkinInfluenceJoints", command=lambda a:mo_riggUtils.getSkinInfluenceJoints())
        pm.button(label="getJointChain", command=lambda a:mo_riggUtils.getJointChain())
        pm.button(label="delChildConst", command=lambda a: libUtil.deleteChildrenConstraints())
        

        pm.text(label="")

         #2. Rigg Editing
        pm.setParent(self.UIElements["mainColumn"])
        pm.separator()
        self.UIElements["4"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])


        pm.button(label="createCvControls", command=lambda a:mo_riggUtils.createCvControls(skin=True))
        pm.button(label="alignJ", command=lambda a:mo_riggUtils.alignJ())
        pm.button(label="vecViz", command=lambda a:mo_riggUtils.vecVizObjects(pm.selected()))

        pm.button(label="createIKSpline", command=lambda a:mo_riggUtils.createIKSpline())
        pm.button(label="createJointsAtPos", command=lambda a:mo_riggUtils.createJointsAtPos())
        pm.button(label="splitJnt", command=lambda a:splitJointUI.splitSelJointUI())

        pm.setParent(self.UIElements["mainColumn"])
        pm.separator()
        self.UIElements["5"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])

        #3. Ctrl Editing
        pm.button(label="cubeCtrl", command=lambda a:mo_riggUtils.createCtrl(shape='cube'))
        pm.button(label="circleCtrl", command=lambda a: mo_riggUtils.createCtrl(shape='circle'))
        pm.button(label="locCtrl", command=lambda a:mo_riggUtils.createCtrl(shape='locator'))

        pm.button(label="grpZERO", command=lambda a:mo_riggUtils.grpCtrl())
        pm.button(label="Scale +", command=lambda a:mo_riggUtils.scaleShape(1.50))
        pm.button(label="Scale -", command=lambda a:mo_riggUtils.scaleShape(0.75))

        pm.setParent(self.UIElements["mainColumn"])
        return self.UIElements["mainColumn"]


    def initializeAnimTab(self, tabHeight, tabWidth):
        columnWidth = 120
        moduleSpecific_scrollHeight = 120
        scrollHeight = tabHeight - moduleSpecific_scrollHeight - 20

        #1. Anim Editing
        self.UIElements["animColumn"] = pm.columnLayout(adj=True, rs=3)

        pm.rowColumnLayout("selsetAddRow", numberOfColumns=3,
                                                  ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)],
                                                  columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)],
                                                  columnWidth=[(1, columnWidth), (2, columnWidth), (3, columnWidth)])
        pm.textField("setName", parent="selsetAddRow")
        pop = pm.popupMenu(parent='setName')

        #pm.optionMenu(label='Colors', changeCommand=lambda a: self.updateTextfield('setName', 'test'))



        pm.button(label="add", parent="selsetAddRow", command=lambda a: self.addSelectionSetWin())
        pm.button(label="remove", parent="selsetAddRow", command=lambda a: self.removeSelectionSetWin())
        pm.setParent(self.UIElements["animColumn"])
        pm.separator()
        pm.text('selectionSets')
        pm.rowLayout("selsetSelRow", numberOfColumns=2, columnWidth2=[300,100], columnAlign=[(1, 'right'),(2, 'left')])
        
        pm.textScrollList("selSetList", parent ="selsetSelRow", width=300, height=100, allowMultiSelection=False,
                          selectCommand=lambda: self.selectSelectionSetWin())
        
        pm.columnLayout("selsetModColumn", parent="selsetSelRow")
        pm.button(label="load", parent ="selsetModColumn", height=22, width=50, command=lambda a: self.loadSelSetWin())
        pm.button(label="delete", parent ="selsetModColumn", height=22, width=50, command=lambda a: self.deleteSelectionSetWin())
        pm.setParent(self.UIElements["animColumn"])

        self.UIElements["1"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])

        pm.button(label="keyRandomizer", command=lambda a:keyRandomizerUI.createUI())
        pm.button(label="set Timesldr Keyrng", command=lambda a:mo_animUtils.setTimesliderToKeyrange())
        pm.button(label="keyEmpty", command=lambda a:mo_animUtils.keyEmpty())

         #2. Rigg Editing
        pm.setParent(self.UIElements["animColumn"])
        pm.separator()
        self.UIElements["2"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])

        pm.button(label="copyKey", command=lambda a:pm.copyKey())
        pm.button(label="pasteKey", command=lambda a:pm.pasteKey())
        pm.button(label="cutKey", command=lambda a:pm.cutKey())

        pm.button(label="copyKeys", command=lambda a:mo_animUtils.copyKeys())
        pm.button(label="infinity", command=lambda a:mo_animUtils.infinity())
        pm.button(label="Save Pose Shelf", command=lambda a:mo_storePoseToShelf.storePoseToShelf())


        pm.button(label="del Constraints", command=lambda a: mo_riggUtils.deleteChildrenConstraints())
        pm.button(label="keyFlash", command=lambda a:mo_animUtils.keyFlash())
        pm.button(label="keyFastinSlowout", command=lambda a:mo_animUtils.keyFastinSlowout())
        pm.text(label="")

        pm.setParent(self.UIElements["animColumn"])
        pm.separator()
        self.UIElements["3"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])

        #3. Ctrl Editing
        pm.button(label="straightMotion", command=lambda a:straightMotion.straightMotion())
        pm.button(label="placeHolderLoc", command=lambda a:libUtil.createPlaceHolder(cnx=0))
        pm.button(label="IkFk Snap UI", command=lambda a:mog_ikFkSwitch.FkIk_UI())

        pm.setParent(self.UIElements["animColumn"])
        return self.UIElements["animColumn"]

    def loadSelSetWin(self):
        quicksets = mo_animUtils.getQuickSelSets()
        for sceneSet in quicksets:
            pm.menuItem('%s_menu'%sceneSet, l=sceneSet, command= pm.Callback(self.updateTextfield, 'setName', sceneSet) )
        if len(quicksets) > 0:
            pm.textScrollList("selSetList", e=1, append=quicksets)

    def updateTextfield(self, name, text):
        pm.textField(name, e=1, text=text)

    def initializeDisplayTab(self, tabHeight, tabWidth):
        columnWidth = 120
        moduleSpecific_scrollHeight = 120
        scrollHeight = tabHeight - moduleSpecific_scrollHeight - 20

        #1. Anim Editing
        self.UIElements["displayColumn"] = pm.columnLayout(adj=True, rs=3)
        self.UIElements["d1"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])

        pm.button(label="Layout Outliner", command=lambda a:mo_displayUtil. layoutCleanOutliner(name='cleanPersp/Outliner'))
        pm.button(label="Layout Anim", command=lambda a: mo_displayUtil.layoutCleanAnim(name='cleanOutliner/Persp/Graph'))
        pm.button(label="Layout Script", command=lambda a: mo_displayUtil.layoutCleanScripting(name='cleanOutliner/Persp/ScriptEditor'))

        pm.button(label="Viz Curves", command=lambda a:mo_displayUtil.toggleCurvesVisibility())
        pm.button(label="Viz Geo", command=lambda a: mo_displayUtil.toggleGeometryVisibility())
        pm.button(label="Viz Flat", command=lambda a: mo_displayUtil.toggleFlatShaded())

         #2. Selection
        pm.setParent(self.UIElements["displayColumn"])
        pm.separator()
        self.UIElements["d2"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])

        pm.button(label="selectHrchy All", command=lambda a:mo_displayUtil.selectHierarchy())
        pm.button(label="selectHrchy Ctl", command=lambda a: mo_displayUtil.selectHierarchy())
        pm.button(label="selectHrchy Jnt", command=lambda a: mo_displayUtil.selectHierarchy())

        # pm.button(label="getDisplayLayer", command=lambda a:mo_displayUtil.getDisplayLayer())
        # pm.button(label="deleteRefEdits", command=lambda a:mo_displayUtil.deleteRefEdits())
        # pm.button(label="deleteRefEdits", command=lambda a: mo_displayUtil.deleteRefEdits())

        pm.button(label="disconnectShaders", command=lambda a:mo_displayUtil.disconnectShaders())
        pm.button(label="viewportSnapshot", command=lambda a:mo_displayUtil.viewportSnapshot())
        pm.button(label="removeNameSpace", command=lambda a:mo_stringUtils.removeNameSpace())

        #3. Ctrl Editing
        pm.button(label="list_duplicates", command=lambda a:mo_stringUtils.list_duplicates())
        pm.button(label="renameDuplicates", command=lambda a:mo_stringUtils.renameDuplicates())
        pm.button(label="ipm", command=lambda a:mo_imageplaneManager.ImagePlaneMngWindow.showUI())

        pm.button(label="lightRigg", command=lambda a:mo_lightRigg.createLightRigg(size=10, lightsTop=3, keyTop=[1], fillTop=[2,3],lightsBottom=4))
        pm.text(label="")
        pm.text(label="")
        #pm.setParent(self.UIElements["displayColumn"])
        #pm.separator()
        #self.UIElements["d3"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])

        pm.setParent(self.UIElements["displayColumn"])
        return self.UIElements["displayColumn"]

    def initializeModelTab(self, tabHeight, tabWidth):
        columnWidth = 120
        moduleSpecific_scrollHeight = 120
        scrollHeight = tabHeight - moduleSpecific_scrollHeight - 20

        
        self.UIElements["modelColumn"] = pm.columnLayout(adj=True, rs=3)
        self.UIElements["m1"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])


        # Pivots
        pm.button(label="Origin Pivot", command=lambda a: mo_alignUtils.movePivot(pm.selected(), moveto="zero"))
        pm.button(label="Min Y Pivot", command=lambda a: mo_alignUtils.movePivot(pm.selected(), moveto="minY"))
        pm.button(label="Center Pivot", command=lambda a: mo_alignUtils.movePivot(pm.selected(), moveto="center"))
        # Pivots
        pm.button(label="Seperate", command=lambda a: mo_meshUtils.separateGeo(objArray = pm.selected(), geoSuffix = 'geo', grpSuffix = 'grp', grp=1, centerPivot=1))
        pm.button(label="Combine", command=lambda a:mo_meshUtils.combineGeo(pm.selected()))
        pm.button(label="Move to Orig", command=lambda a: mo_alignUtils.moveToZero(pm.selected()))

        # Shader assign
        pm.textField("shaderName", width=columnWidth * 0.3)
        pm.optionMenu( width= columnWidth * 0.3)
        pm.menuItem(label='Blinn')
        pm.menuItem(label='Lmbert')
        pm.button(label="Assign Shader", command=lambda a: mo_shaderUtils.assignNewMaterial(
            name=pm.textField("shaderName", q=1, text=1), color=[0.5,0.5,0.5], shader="blinn", target=pm.selected()))

        # Tempimport/Export
        pm.textField("tempExportPath", width=columnWidth * 0.3, text=mo_UI.getHomeDir(subfolder='maya/tempExport'))
        pm.button(label="Temp Export", command=lambda a: mo_fileSystemUtils.tempExportSelected(path=pm.textField("tempExportPath", q=1, text=1)))
        pm.button(label="Temp Import", command=lambda a: mo_fileSystemUtils.tempImport(path=pm.textField("tempExportPath", q=1, text=1)))

        # "C:\Users\dellPC\Documents\maya\tempExport"

        pm.setParent(self.UIElements["modelColumn"])
        return self.UIElements["modelColumn"]

    @staticmethod
    def getHomeDir(subfolder='Documents'):
        from os.path import expanduser
        home = expanduser("~")
        homedirsubfolder = home + '/' +subfolder
        return homedirsubfolder

    def inputSelTfb(self, name):
        if len(pm.selected()) == 0:
            pm.textFieldButtonGrp(name, e=1, tx='')
            return []
        pm.textFieldButtonGrp(name, e=1, tx=pm.selected()[0])


    def inputChannelboxSelectionTbf(self, name):
        channelBox = pm.mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')	#fetch maya's main channelbox
        attrs = pm.channelBox(channelBox, q=True, sma=True)
        print 'attributes selected are %s'%attrs

        if not attrs:
            pm.textFieldButtonGrp(name, e=1, tx='')
            return []
        if len(attrs) is not 1:
            pm.warning('Highlight only the IK/FK Switch Attribute in the Channelbox')
            return []
        pm.textFieldButtonGrp(name, e=1, tx=attrs[0])
        return attrs

    def addSelectionSetWin(self):
        setInput = pm.textField("setName", q=1, tx=1)
        if pm.objExists(setInput) == False:
            pm.sets(n=setInput)
            pm.textScrollList("selSetList", e=1, append=setInput)

        pm.sets(setInput, add=pm.selected())



    def removeSelectionSetWin(self):
        setInput = pm.textField("setName", q=1, tx=1)
        if pm.objExists(setInput):
            pm.sets(setInput, remove=pm.selected())
    def selectSelectionSetWin(self):
        selSet =  pm.textScrollList("selSetList", query=1, selectItem=1  )
        print 'Selset %s'%selSet
        pm.select(pm.sets(selSet, q=1))
        return 'a'

    def deleteSelectionSetWin(self):
        selSet = pm.textScrollList("selSetList", query=1, selectItem=1)
        pm.delete(selSet)
        pm.textScrollList("selSetList", e=1, removeItem=selSet)

    def getAndCheckInputWin(self):
        fkshldr = pm.textFieldButtonGrp("fkshldrTfb", q=1, tx=1)
        fkellbow = pm.textFieldButtonGrp("fkellbowTfb", q=1, tx=1)
        fkwrist = pm.textFieldButtonGrp("fkwristTfb", q=1, tx=1)
        ikwrist = pm.textFieldButtonGrp("ikwristTfb", q=1, tx=1)
        ikpv = pm.textFieldButtonGrp("ikpvTfb", q=1, tx=1)
        switchCtrl = pm.textFieldButtonGrp("switchCtrlTfb", q=1, tx=1)
        switchAttr = pm.textFieldButtonGrp("switchAttrTfb", q=1, tx=1)
        switch0isfk = pm.radioCollection("switch0isfkTfb", q=1, sl=1)


        for input in [fkwrist, fkellbow, fkshldr, ikwrist, switchCtrl]:
            if len(input) == 0:
                pm.error('Empty input field found %s. Aborting.'%input)
                return False
            if pm.objExists(input) == 0:
                pm.error('Input Ctrl %s does not exist. Aborting'%input)
                return False
        # IK PIV can stay empty...
        ###TODO how to align with fk if there is no pv in ik
        if pm.objExists(ikpv) == 0:
            pm.error('Input Piv %s does not exist. Aborting'%input)
            return False

        rotOffsetX = pm.textField('rotOffsetX', q=1, tx=1)
        try:
            rotOffsetX = int(rotOffsetX)
        except:
            rotOffsetX = 0
            pass
        rotOffsetY = pm.textField('rotOffsetY', q=1, tx=1)
        try:
            rotOffsetY = int(rotOffsetY)
        except:
            rotOffsetY = 0
            pass
        rotOffsetZ = pm.textField('rotOffsetZ', q=1, tx=1)
        try:
            rotOffsetZ = int(rotOffsetZ)
        except:
            rotOffsetZ = 0
            pass
        rotOffset=[rotOffsetX, rotOffsetY, rotOffsetZ]

        return fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, rotOffset

    def saveIkFkCtrlsWin(self):
        limbRadio = pm.radioCollection("limbRadioColl", q=1, sl=1)
        print 'limbradio is %s'%limbRadio
        if limbRadio == 'NONE':
            pm.warning('Limb choice missing. Please choose form the UI options')
            return False
        limb = limbRadio.split('_')[-1]
        side = limbRadio.split('_')[0]

        fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, rotOffset = self.getAndCheckInputWin()

        mo_ikFkSwitch.saveIKFkCtrls(limb, side, fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, rotOffset)

    def loadIkFkCtrlsWin(self):
        print 'loading fkikCtrls '
        limbRadio = pm.radioCollection("limbRadioColl", q=1, sl=1)
        limb = limbRadio.split('_')[-1]
        side = limbRadio.split('_')[0]
        if len(pm.selected()) == 0:
            pm.warning('Select anything from the rigg')
            return False
        ns = pm.selected()[0].split(':')[0]

        print limb, side
        storedic = mo_ikFkSwitch.loadIkFkCtrl(ns, limb, side)
        for attrName, value in storedic.items():
            if attrName is 'switch0isfk':
                if value is 'attr0IsFk':
                    pm.radioCollection("switch0isfkTfb", e=1, select='attr0IsIk')
                else:
                    pm.radioCollection("switch0isfkTfb", e=1, select='attr0IsFk')
            else:
                pm.textFieldButtonGrp("%sTfb"%attrName, e=1, tx=value)

    def switchFkIkWin(self):
        try:
            fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, rotOffset = self.getAndCheckInputWin()
        except:
            print 'input error'
            return
        rotOffsetX = pm.textField('rotOffsetX', q=1, tx=1)
        if rotOffsetX == '' : rotOffsetX = 0
        else: rotOffsetX = int(rotOffsetX)
        rotOffsetY = pm.textField('rotOffsetY', q=1, tx=1)
        if rotOffsetY == '' : rotOffsetY = 0
        else: rotOffsetY = int(rotOffsetY)
        rotOffsetZ = pm.textField('rotOffsetZ', q=1, tx=1)
        if rotOffsetZ == '' : rotOffsetZ = 0
        else: rotOffsetZ = int(rotOffsetZ)

        mo_ikFkSwitch.fkikMatch(fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk=switch0isfk,  rotOffset=[rotOffsetX, rotOffsetY, rotOffsetZ])

    def switchIkFkWin(self):

        try:
            fkshldr, fkellbow, fkwrist, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk, rotOffset = self.getAndCheckInputWin()
        except:
            print 'input error'
            return
        rotOffsetX = pm.textField('rotOffsetX', q=1, tx=1)
        if rotOffsetX == '' : rotOffsetX = 0
        else: rotOffsetX = int(rotOffsetX)
        rotOffsetY = pm.textField('rotOffsetY', q=1, tx=1)
        if rotOffsetY == '' : rotOffsetY = 0
        else: rotOffsetY = int(rotOffsetY)
        rotOffsetZ = pm.textField('rotOffsetZ', q=1, tx=1)
        if rotOffsetZ == '' : rotOffsetZ = 0
        else: rotOffsetZ = int(rotOffsetZ)

        mo_ikFkSwitch.ikfkMatch(fkwrist, fkellbow, fkshldr, ikwrist, ikpv, switchCtrl, switchAttr, switch0isfk=switch0isfk,  rotOffset=[rotOffsetX, rotOffsetY, rotOffsetZ])






def tempExportSelected(save_name = 'tempExport', path = "U:/personal/Monika/tempExport" ):
    pm.cmds.file("%s/%s.ma"%(path,save_name), pr=1, typ="mayaAscii", force=1, options="v=0;", es=1)
