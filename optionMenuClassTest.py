def createUI():
        WINDOW_NAME = 'classTest'
        WINDOW_TITLE = 'classTest'
        WINDOW_SIZE = (310,200)
        
        ## destroy the window if it already exists
        try:
            pm.deleteUI(WINDOW_NAME, window=True)
        except: pass
        # draw the window
        WINDOW_NAME = pm.window(WINDOW_NAME,title=WINDOW_TITLE,widthHeight=WINDOW_SIZE,sizeable = False)
        mainForm = pm.rowLayout(nc=2)
        #create class obj
        c = Ant('myAnt')
        
        gearOptionMenu=pm.optionMenu(
            label='Gearlists',
            width=200
        )
        gear_option_list(gearOptionMenu)
        
        c.setOptionMenu(gearOptionMenu)
        c.gear = pm.optionMenu(gearOptionMenu, q=1, v=1)
        
        
        
        go_btn = pm.button(label='go',  command=pm.Callback(c.updateGear))
        pm.setParent(mainForm)
        pm.showWindow()
        
createUI()

def gear_option_list(menu, *args):
    #clear array and optionMenu
   
   menu.clear()
   listOfGears= ['gear1', 'gear2', 'gear3']
   pm.menuItem(l='None', parent=menu)
   
   for item in listOfGears:
         pm.menuItem(l=item, parent=menu)
         
class Ant():
    def __init__(self, name):
        self.name = name
        self.gear = None
        self.gearOptionMenu = None
        
    def setOptionMenu(self, optionM):
        self.gearOptionMenu = optionM
        
    def updateGear(self):
        print self.gear
        print pm.optionMenu(self.gearOptionMenu, q=1, v=1)