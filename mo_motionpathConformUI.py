import os
import pymel.core as pm
"""
mermaid_motionPathConform

"""
import mo_motionpathConform06 as mermaid
reload(mermaid)
#import riggTool.custom.mermaidMotionPath as mermaid
#reload(mermaid)

mainWin='mermaidMainWindow'
def mermaidUI():
    if(pm.window(mainWin, ex=1)):
        pm.deleteUI(mainWin)
    pm.window(mainWin, t='mermaidMainWindow', widthHeight=(380,500))
    pm.scrollLayout( h=700,w=380, vis=1)
    #load active agent Name
    pm.separator(h=10,style='none',w=380)
    mainUI=pm.columnLayout(w=380,cal='center',adj=1)
    pm.separator(h=5,style='none',w=380)

    ###################content#############################
    ##########################################
    #1. import puppet
    pm.text(l='STEP 1.',al='center')
    pm.button(c=lambda x:  mermaid.importRigPuppet(),l='import puppet',h=25)

    ##########################################
    #2. create path
    pm.separator(h=5,style='single',w=380)
    pm.text(l='STEP 2.',al='center')

    sectionsInput = pm.intSliderGrp('numCtrls',fmx=20,
        min=1,
        max=20,
        cw3=(110, 40, 165),
        value=4,
        label='  numCtrl',
        fmn=1,
        field=True,
        cal=(1, 'left'),
        adj=3)

    directionInput = pm.textFieldGrp('direction',cw=[(1, 110), (2, 70), (3, 70)],
        cal=(1, 'left'),
        text="+x",
        adj=3,
        label=' start frame:')
    pm.button(c=lambda motionCurve: mermaid.createMotionTrail(sections=sectionsInput.getValue(), direction=directionInput.getText()),l='create path',h=25)
   
    ##########################################
    #3. rebuild path
    pm.separator(h=10,style='single',w=380)
    pm.text(l='STEP 3.',al='center')

    pm.intSliderGrp('rebuildCtrls',fmx=20,
        min=1,
        max=20,
        cw3=(110, 40, 165),
        value=4,
        label='  numCtrl',
        fmn=1,
        field=True,
        cal=(1, 'left'),
        adj=3)
    motionCurve = ""
    attachObj = ""
    pm.button(c=lambda attachObj: mermaid.importRigPuppet(),l='rebuild path',h=25)
    pm.button(c=lambda attachObj: mermaid.resetMotionTrail(),l='reset path',h=25)
    
    ##########################################
    #4. connect puppet to path
    pm.separator(h=5,style='single',w=380)
    pm.text(l='STEP 4.',al='center')

    startframeInput = pm.intFieldGrp('start',cw=[(1, 110), (2, 70), (3, 70)],
        cal=(1, 'left'),
        value1=970,
        adj=3,
        label=' start frame:')
    endframeInput = pm.intFieldGrp('end',cw=[(1, 110), (2, 70), (3, 70)],
        cal=(1, 'left'),
        value1=1500,
        adj=3,
        label=' end frame:')
    
    pm.button(c=lambda x: mermaid.motionpathConformObject(motionCurve, attachObj, starttime=startframeInput.getValue(),endtime=endframeInput.getValue()),l='connect to path',h=25)

    ##########################################
    #5. snap rit to puppet
    pm.separator(h=5,style='single',w=380)
    pm.text(l='STEP 5.',al='center')

    pm.button(c=lambda x:  mermaid.snapMermaid(),l='snap rigg to puppet',h=25)

    pm.showWindow(mainWin)
    #allowedAreas = ['right', 'left',"top", "bottom"]
    #pm.dockControl( area='right', content=mainWin, allowedArea=allowedAreas )

mermaidUI()
# end