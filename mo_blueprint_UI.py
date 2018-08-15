import pymel.core as pm
import System.utils as utils
import maya.cmds as cmds
from functools import partial

reload(utils)

class Blueprint_UI:
    def __init__(self):
        #Store UI elements in a dictionary
        self.UIElements = {}
        
        if pm.window("blueprint_UI_window", exists=True):
            pm.deleteUI("blueprint_UI_window")
        self.windowWidth = 400
        self.windowHeight = 598
        
        self.UIElements["window"] = pm.window("blueprint_UI_window", width=self.windowWidth, height=self.windowHeight, title="blueprint_UI_window")
        
        self.UIElements["topLevelColumn"] = pm.columnLayout(adjustableColumn=True, columnAlign="center")
        
        #Setup Tabs #every child creates new tab
        tabHeight = 500
        self.UIElements["tabs"] = pm.tabLayout(height=tabHeight, innerMarginWidth=5, innerMarginHeight=5)
        tabWidth = pm.tabLayout(self.UIElements["tabs"], q=True, width=True)
        tabWidth = 400
        self.scrollWidth = tabWidth - 40
        
        self.initializeModuleTab(tabHeight, tabWidth)
        pm.tabLayout(self.UIElements["tabs"], edit=True, tabLabelIndex=([1, "Modules"]))   
        
        #3. Lock and Publish Buttons
        pm.setParent(self.UIElements["topLevelColumn"])
        self.UIElements["lockPublishColumn"] = pm.columnLayout(adj=True, columnAlign="center", rs=3)#single column
        pm.separator()
        self.UIElements["lockBtn"] = pm.button(label="Lock",  command=partial(self.lock))
        pm.separator()
        self.UIElements["publishBtn"] = pm.button(label="Publish")
        pm.separator()
        
        #Display window
        pm.showWindow(self.UIElements["window"])
        
    def initializeModuleTab(self, tabHeight, tabWidth):
        moduleSpecific_scrollHeight = 120
        scrollHeight = tabHeight - moduleSpecific_scrollHeight - 20
        #1. Module Creation
        self.UIElements["moduleColumn"] = pm.columnLayout(adj=True, rs=3)
        ##column layout for all controls, symbols and buttons 
        self.UIElements["moduleFrameLayout"] = pm.frameLayout(height=200, collapsable=False, borderVisible=False, labelVisible=False)
        ##scroll bar on side, scroll layout prefers to have single child
        self.UIElements["moduleList_Scroll"] = pm.scrollLayout(hst=0)
        self.UIElements["moduleList_column"]= pm.columnLayout(columnWidth = self.scrollWidth, adj=True, rs=2)
        
        #first seperator
        pm.separator()
        self.UIElements["moduleList_row"] = pm.rowColumnLayout( numberOfColumns=1, columnWidth=(1, self.windowWidth-30) )
        #button for each module
        for module in utils.findAllModules("Modules/Blueprint"):
            self.createModuleInstallButton(module)   
            pm.separator()
        
        #2. Module Editing
        pm.setParent(self.UIElements["moduleColumn"])
        pm.separator()
        self.UIElements["moduleName_row"] = pm.rowLayout(nc=2, columnAttach=(1, "right", 0), columnWidth=[(1, 80)], adjustableColumn=2)
        pm.text(label="Module Name : ")
        self.UIElements["moduleName"] = pm.textField(enable=False, alwaysInvokeEnterCommandOnReturn=True)
        
        pm.setParent(self.UIElements["moduleColumn"])
        columnWidth = (tabWidth - 20) /3
        self.UIElements["moduleButtons_rowColumn"] = pm.rowColumnLayout(numberOfColumns=3, ro=[(1, "both", 2), (2, "both", 2), (3, "both", 2)], columnAttach=[(1, "both", 3), (2, "both", 3), (3, "both", 3)], columnWidth=[(1,columnWidth), (2,columnWidth),(3,columnWidth)])
        
        self.UIElements["rehookBtn"] = pm.button(enable=False, label="Re-hook")
        self.UIElements["snapRootBtn"] = pm.button(enable=False, label="Snap Root-Hook")
        self.UIElements["costrRootBtn"] = pm.button(enable=False, label="Constrain Root-Hook")
        
        self.UIElements["groupSelectedBtn"] = pm.button(label="Group Selected")
        self.UIElements["ungroupBtn"] = pm.button(enable=False, label="Ungroup")
        self.UIElements["mirrorModuleBtn"] = pm.button(enable=False, label="Mirror Module")
        
        pm.text(label="")
        self.UIElements["deleteModuleBtn"] = pm.button(enable=False, label="Re-hook")
        self.UIElements["symmetryMoveCheckBox"] = pm.checkBox(enable=True, label="Symmetry Move")

        pm.setParent(self.UIElements["moduleColumn"])
        pm.separator()
         
        self.UIElements['moduleSpecificRowColumnLayout'] = pm.rowColumnLayout(nr=1, rowAttach=[1, 'both', 0], rowHeight=[1, moduleSpecific_scrollHeight])
        self.UIElements['moduleSpecificScroll'] = pm.scrollLayout(hst=12)
        self.UIElements['moduleSpecificColumn'] = pm.columnLayout(columnWidth=self.scrollWidth, adj=True, columnAttach = ['both', 5], rs=2)
        self.UIElements['test'] = pm.button(enable=False, label="jj")
        pm.setParent(self.UIElements["moduleColumn"])
        
        pm.separator()
        
        
    def createModuleInstallButton(self, module):
        mod = __import__("Blueprint."+module, {}, {}, [module])
        reload(mod)
        
        title = mod.TITLE
        description = mod.DESCRIPTION
        icon = mod.ICON
        buttonSize = 64
        
        pm.rowColumnLayout( numberOfColumns=2, columnWidth=[(1, buttonSize)] )
        #Create UI  #distinguish between buttons with partial functions  
        self.UIElements["module_button_"+module] = pm.symbolButton(width=buttonSize, height=buttonSize, image=icon, command=partial(self.installModule, module))
             
        textColumn = pm.columnLayout(columnAlign="center")
        pm.text(align="left", width=self.windowWidth-30, label=title)
        pm.scrollField(text=description, editable=False, width=self.windowWidth-30, height=50, wordWrap=True)
        pm.setParent(self.UIElements["moduleList_row"])
      
    def installModule(self, module, *args):
        #1. Create Unique Module Name: name = BlueprintModuleName__UserSpecifiedName:objectName
        basename = "instance_"
        pm.namespace(setNamespace=":")
        namespace = pm.namespaceInfo(listOnlyNamespaces=True)
        
        #1a. search existing namespaces for all that have __UserSpecifiedName
        for i in range(len(namespace)):
            #index of first occurence, find __, if found
            if namespace[i].find("__") != -1:
                namespace[i] = namespace[i].partition("__")[2]
                
        #1b. create unique UserSpecifiedName  (get hightest digit that exists and add 1)
        newSuffix =  utils.findHeighestTrailingNumber(namespace, basename) + 1
        userSpecName = basename + str(newSuffix)
    
        #import module
        mod = __import__("Blueprint."+module, {}, {}, [module])
        reload(mod)
        #create class reference from string (without ())
        moduleClass = getattr(mod, mod.CLASS_NAME)
        #with class reference, call constructor and istall method of this module
        moduleInstance = moduleClass(userSpecName)
        moduleInstance.install()
        
        moduleTransform = mod.CLASS_NAME + "__" + userSpecName + ":module_transform"
        pm.select(moduleTransform, replace=True)
        pm.setToolTo("moveSuperContext")
    
    def lock(self, *args):
        result = pm.confirmDialog(messageAlign='center', title='Lock Blueprints', message='Locking will convert modules to joints. This action can not bet undone. \n Modification to blueprint system can not be done after this.', button=['Accept', 'Cancel'], defaultButton='Accept', cancelButton='Cancel')
        if result != 'Accept':
            return
        
        moduleInfo = [] #store (module, userSpecifiedName) pairs
        
        #find all modules in scene and store them in moduleInfo list [moduleName, userSpecifiedName]
        pm.namespace(setNamespace=":") 
        namespace = pm.namespaceInfo(listOnlyNamespaces=True)
        moduleNameInfo = utils.findAllModuleNames("/Modules/Blueprint")
        validModules = moduleNameInfo[0]
        validModuleNames = moduleNameInfo[1]
        
        for n in namespace:
            splitString = n.partition("__")
            
            if splitString[1] != "":
                module = splitString[0]
                userSpecifiedName = splitString[2]
                
                if module in validModuleNames:
                    index = validModuleNames.index(module)
                    moduleInfo.append([validModules[index], userSpecifiedName])
        if len(moduleInfo) == 0:
            pm.confirmDialog(messageAlign='center', title='Lock Blueprints', message='No Blueprint Modules in scene', button=['Accept'], defaultButton='Accept')
            return
        print moduleInfo
        moduleInstances= []
        
        #lock phase 1 - gather tranform/rotation info of joints
        for module in moduleInfo:
            mod = __import__('Blueprint.'+module[0], {}, {}, [module[0]])
            reload(mod)
            moduleClass = getattr(mod, mod.CLASS_NAME)
            moduleInst = moduleClass(userSpecifiedName=module[1])  
            moduleInfo = moduleInst.lock_phase1()
            moduleInstances.append((moduleInst, moduleInfo))
            print moduleInfo
            
        #lock phase 2
        for module in moduleInstances:
            module[0].lock_phase2(module[1])
    