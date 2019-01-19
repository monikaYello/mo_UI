import pymel.core as pm
import sys
import os
import maya.cmds as cmds

myScriptPath = 'D:/Google Drive/PythonScripting/scripts'
if (not myScriptPath in sys.path):
    sys.path.insert(0,myScriptPath)

import mo_Utils.mo_fileSystemUtils as mo_fileSystemUtils
import mo_Utils.mo_dynamicUtils as mo_dynamicUtils
reload(mo_dynamicUtils)


tempExportDir = 'D:\\temp'


class mo_dyn_UI:
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

        riggTab = self.initializeParticleTab(tabHeight, tabWidth)
        pm.setParent("..")
        animTab = self.initializeClothTab(tabHeight, tabWidth)
        pm.tabLayout(self.UIElements["tabs"], edit=True, tabLabel=((riggTab, 'mo_particle'), (animTab, 'mo_cloth')))

        #Display window
        pm.showWindow(self.UIElements["window"])

    def initializeParticleTab(self, tabHeight, tabWidth):
        tab = 'particle'
        columnWidth = 100
        moduleSpecific_scrollHeight = 120
        scrollHeight = tabHeight - moduleSpecific_scrollHeight - 20

        self.UIElements["%smainCol"%tab] = pm.columnLayout("%smainCol"%tab)
        pm.rowColumnLayout("%sCreationCol"%tab, numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])
        
        # 1. particle creation
        pm.button(label="tempExport", command=lambda a:mo_fileSystemUtils.tempExportSelected(path = tempExportDir))
        pm.button(label="tempImport", command=lambda a:mo_fileSystemUtils.tempImport(path = tempExportDir))
        pm.button(label="tempExportUI", command=lambda a:mo_fileSystemUtils.tempExportSelected(path = tempExportDir))
        
        pm.button(label="create Passive", command=lambda a:mo_dynamicUtils.createPassiveCollider()())
        pm.button(label="create volumeCrv", command=lambda a:mo_dynamicUtils.createVolumeCrv())
        pm.button(label="create volumeCrv", command=lambda a:mo_dynamicUtils.createVolumeCrv())

        pm.setParent(self.UIElements["%smainCol"%tab])
        pm.separator()
        pm.rowColumnLayout("%sEditCol"%tab, numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])
   
        # 2. particle edit
        pm.button(label="connectVisibility", command=lambda a:mo_dynamicUtils.connectVisibilityToIsDynamic()())
        pm.button(label="transferAttr", command=lambda a:mo_dynamicUtils.transferAttrs(pm.selected()[0], pm.selected()[1:]))
        pm.button(label="---")

        pm.setParent(self.UIElements["%smainCol"%tab])
        return self.UIElements["%smainCol"%tab]

    def initializeClothTab(self, tabHeight, tabWidth):
        columnWidth = 100
        moduleSpecific_scrollHeight = 120
        scrollHeight = tabHeight - moduleSpecific_scrollHeight - 20
        tab = 'cloth'

        #1. Get Info
        self.UIElements["%smainCol"%tab] = pm.columnLayout("%smainCol"%tab)
        pm.rowColumnLayout("snapRowColumn", numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])
        
        pm.button(label="tempExport", parent="snapRowColumn", command=lambda a:mo_fileSystemUtils.tempExportSelected(path = tempExportDir))
        pm.button(label="tempImport", parent="snapRowColumn", command=lambda a:mo_fileSystemUtils.tempImport(path = tempExportDir))
        pm.button(label="tempExportUI", parent="snapRowColumn", command=lambda a:mo_fileSystemUtils.tempExportSelected(path = tempExportDir))
        
        pm.button(label="create Passive", command=lambda a:mo_dynamicUtils.createPassiveCollider()())
        pm.button(label="create volumeCrv", command=lambda a:mo_dynamicUtils.createVolumeCrv())
        pm.button(label="create volumeCrv", command=lambda a:mo_dynamicUtils.transferAttrs())

        #pm.setParent(self.UIElements["mainCol"])
        pm.separator()

        pm.button(label="connectVisibility", command=lambda a:mo_dynamicUtils.connectVisibilityToIsDynamic()())
        pm.button(label="transferAttr", command=lambda a:mo_dynamicUtils.transferAttrs())
        pm.button(label="transferAttr", command=lambda a:mo_dynamicUtils.transferAttrs())

        pm.setParent(self.UIElements["%smainCol"%tab])
        return self.UIElements["%smainCol"%tab]

