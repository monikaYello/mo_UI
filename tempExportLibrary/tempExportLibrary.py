import Qt
import maya.cmds as cmds
import os
import json
import pprint
'''
import mo_UI.tempExportLibrary.libraryUI as libraryUI
reload(libraryUI)
libraryUI.TempExportLibraryUI().show()
'''


USERAPPDIR = "//192.168.120.60/3d/3D_Library/"
print USERAPPDIR
DIRECTORY = os.path.join(USERAPPDIR, 'Temp_Exporter')
# join will give us correct OS secific slashes


def createDirectory(directory=DIRECTORY):
    if not os.path.exists(directory):
        os.mkdir(directory)

class TempExportLibrary(dict):

    def save(self, name, directory=DIRECTORY, screenshot=True, **info):
        # info will be dictionary
        print info

        createDirectory(directory)

        path = os.path.join(directory, '%s.ma'%name)
        infoFile = os.path.join(directory, '%s.json'%name)

        cmds.file(rename=path)
        if cmds.ls(selection=True):
            cmds.file(exportSelected=True, force=True, type='mayaAscii')
        else:
            cmds.file(save=True, type="mayaAscii", force=True)

        print ' saving file. info is %s'%info
        if screenshot:
            info["screenshot"] = self.saveScreenShot(name, directory=directory)
        with open(infoFile, 'w') as f:
            json.dump(info, f, indent=4)

        self[name] = info

    def find(self, directory=DIRECTORY):
        # exit if dir not exists
        self.clear()
        if not os.path.exists(directory):
            return

        files = os.listdir(directory)
        # get only .ma files
        mayaFiles = [f for f in files if f.endswith('.ma')]

        for ma in mayaFiles:

            name, ext = os.path.splitext(ma)

            path = os.path.join(directory, ma)

            infoFile = '%s.json' %name

            if infoFile in files:
                infoFile = os.path.join(directory, infoFile)

                with open(infoFile, 'r') as f:
                    info = json.load(f)
                    pprint.pprint(info)
            else:
                info = {}
                #print "No info found"

            screenshot = '%s.jpg'%name
            if screenshot in files:
                info['screenshot'] = os.path.join(directory,name) + '.jpg'

            info['name'] = name
            info['path'] = path

            self[name] = info

        #pprint.pprint(self)


    def load(self, name):
        path = self[name]['path']
        cmds.file(path, i=True, usingNamespaces=False)

    def delete(self,name):

        try:
            os.remove(self[name]['path'])
        except:
            print 'file not found'

        try:
            os.remove(self[name]["screenshot"])
        except:
            print 'no screenshot found'
            
        try:
            os.remove(self[name]["path"].replace('.ma', '.json'))
        except:
            print 'no json found'
            

    def saveScreenShot(self, name, directory=DIRECTORY):
        path = os.path.join(directory, '%s.jpg'%name)
        cmds.viewFit()
        cmds.setAttr('defaultRenderGlobals.imageFormat', 8)
        cmds.playblast(completeFilename=path, forceOverwrite=True, format='image', width=200, height=200,
                       showOrnaments = False, startTime=1, endTime=1, viewer=False )
        return path
