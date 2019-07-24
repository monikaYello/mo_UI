import pprint
from maya import cmds
import Qt
import logging
from maya import OpenMayaUI as omui

logging.basicConfig()
logger = logging.getLogger('LightingManager')
logger.setLevel(logging.DEBUG)
'''
import mo_UI.tempExportLibrary.libraryUI as libraryUI
reload(libraryUI)
libraryUI.TempExportLibraryUI().show()
'''

from maya import OpenMayaUI as omui
#from Qt import QtWidgets, QtCore, QtGui
from PySide2 import QtWidgets, QtCore, QtGui

if Qt.__binding__ == 'PySide':
    logger.debug('Using Pyside with shiboken')
    from shiboken import wrapInstance
    from Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    logger.debug('Using PyQt with sip')
    from sip import wrapinstance as wrapInstance
    from Qt.QtCore import pyqtSignal as Signal
else:
    logger.debug('Using Pyside2 with shiboken')
    from shiboken2 import wrapInstance
    from Qt.QtCore import Signal

def getMayaMainWindow():
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr

import tempExportLibrary
reload(tempExportLibrary)

class TempExportLibraryUI(QtWidgets.QDialog):
    """
    The TempExportLibraryUI is a dialog that lets us save and import controllers
    """
    def __init__(self):
        parent = getMayaMainWindow()
        super(TempExportLibraryUI, self).__init__(parent=parent)
        self.setWindowTitle("Controller Library UI")
        # The libarry variable points to an instance of our controller library
        self.library = tempExportLibrary.TempExportLibrary()

        # Every time we creat a new instance, we will automatically build our UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """ This method builds our UI """

        print "Building UI"
        ptr = omui.MQtUtil.mainWindow()
        self.parent_widget = ptr
        layout = QtWidgets.QVBoxLayout(self)

        saveWidget = QtWidgets.QWidget()
        saveLayout = QtWidgets.QHBoxLayout(saveWidget)

        layout.addWidget(saveWidget)

        self.saveNameField = QtWidgets.QLineEdit()
        saveLayout.addWidget(self.saveNameField)

        saveBtn = QtWidgets.QPushButton('Save')
        saveBtn.clicked.connect(self.save)
        saveLayout.addWidget(saveBtn)

        # parameters for our thumbnail size
        size =64
        buffer = 12

        # grid list widget to display our controller thumbnails
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget.setViewMode(QtWidgets.QListWidget.IconMode)
        self.listWidget.setIconSize(QtCore.QSize(size, size))
        self.listWidget.setResizeMode(QtWidgets.QListWidget.Adjust)
        self.listWidget.setGridSize(QtCore.QSize(size+buffer, size+buffer))

        layout.addWidget(self.listWidget)

        # button widget
        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        importBtn = QtWidgets.QPushButton('Import')
        importBtn.clicked.connect(self.load)
        btnLayout.addWidget(importBtn)

        refresBtn = QtWidgets.QPushButton('Refresh')
        refresBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refresBtn)

        closeBtn = QtWidgets.QPushButton('Close')
        closeBtn.clicked.connect(self.close)
        btnLayout.addWidget(closeBtn)


    def populate(self):
        """ This clears list widget and re- popoulates it with items of controller """

        self.listWidget.clear()
        self.library.find()
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            #self.listWidget.itemClicked.connect(self.printTest)
            self.listWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
            self.listWidget.customContextMenuRequested.connect(self.on_context_menu)
            # create context menu
            
            self.popMenu = QtWidgets.QMenu(self)
            action = QtWidgets.QAction('delete', self)
            self.popMenu.addAction(action)
            # self.popMenu.addAction(QtWidgets.QAction('test1', self))
            # self.popMenu.addSeparator()
            # self.popMenu.addAction(QtWidgets.QAction('test2', self))
            action.triggered.connect(lambda: self.delete(name))

            self.listWidget.addItem(item)
            screenshot = info.get('screenshot')
            if screenshot:
                icon = QtGui.QIcon(screenshot)
                item.setIcon(icon)
            #self.listWidget.itemClicked(self.mousePressEvent)
            item.setToolTip(pprint.pformat(info))

    def load(self):
        """ Loads the currently selected controller """

        currentItem = self.listWidget.currentItem()
        if not currentItem:
            return
        name = currentItem.text()
        self.library.load(name)

    def save(self):
        """ Save the controller with the given file name"""

        name = self.saveNameField.text()
        print 'Name', name
        if not name.strip():
            cmds.warning("You must enter a Name!")
            return
        self.library.save(name)
        self.populate()
        self.saveNameField.setText('')

    def printTest(self):
        print 'test'

    def on_context_menu(self, point):
        # show context menu
        self.popMenu.exec_(self.listWidget.mapToGlobal(point))

    def delete(self, item):
        print 'deleting item:%s'%item
        #self.library.delete(item)
        self.populate()
        self.popMenu.close()


