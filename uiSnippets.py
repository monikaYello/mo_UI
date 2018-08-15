### TAB LAYOUT ###
'''
winID = "kevsTabWin"
if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

# Create the window
cmds.window(winID,t="tabs")

# Create the tabLayout
tabControls = cmds.tabLayout()

# Create the first tab UI
tab1Layout = cmds.columnLayout()
cmds.button()
cmds.textField()

# We need to go back one to the tabLayout (the parent)
# to add the next tab layout.
cmds.setParent('..')

# Create the second tab UI
tab2Layout = cmds.columnLayout()
cmds.button()
cmds.textField()
cmds.setParent('..')

# Create appropriate labels for the tabs
cmds.tabLayout(tabControls, edit=True, tabLabel=( (tab1Layout,"Welcome"),(tab2Layout,"Human") ) )

# Display the UI
cmds.showWindow(winID)
'''


### FRAME LAYOUT ###
'''
import maya.cmds as cmds

winID = "kevsFrameWin"
if cmds.window(winID, exists=True):
    cmds.deleteUI(winID)

# Create the window
cmds.window(winID,t="frames")

# Create a 'container' Layout to keep our frames in
rootLayout = cmds.columnLayout()

# Create a frame layout. Note that I am not declaring a
# variable here as frameLayout are only supposed to
# support a single child, and our child will be another
# layout...  So we really want to reference the child
# rather then the frameLayout parent anyway.
cmds.frameLayout( label="Top frame" )

# Generate a child Layout inside the frame.
# declare a variable here as it will allow us to reference
# contents inside our frame (within this layout).
frameOne = cmds.columnLayout()
cmds.button( label='A button in frame one')

# Jump back to our root container Layout to add a new Frame
# If we were to use the '..' approach, we would need *2* of
# them to get back to the root.
#
# '..' back to the frame parent, then '..' to the root parent
cmds.setParent(rootLayout)

# Next frame layout.  This one we will make collapsable
cmds.frameLayout( label="Collapsable frame", collapsable=True )

# As per the first frame, generate our child layout
frameTwo = cmds.columnLayout()
cmds.text(label="Here's some nice buttons for you to click")
cmds.button( label='Another button' )
cmds.button( label='Yes, a button' )
cmds.button( label='Maybe 3 is enough' )

# To add more, we need to follow the same process. setParent,
# frameLayout, columnLayout, controls inside frame...

# Display the UI
cmds.showWindow(winID)'''