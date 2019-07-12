import pprint

from maya import cmds

import tempExportLibrary
reload(tempExportLibrary)


#from Qt import QtWidgets, QtCore, QtGui
from PySide2 import QtWidgets, QtCore, QtGui

class ControllerLibraryUI(QtWidgets.QDialog):
    """
    The TempExportLibraryUI is a dialog that lets us save and import controllers
    """
    def __init__(self):
        super(ControllerLibraryUI, self).__init__()
        self.setWindowTitle("Controller Library UI")
        # The libarry variable points to an instance of our controller library
        self.library = tempExportLibrary.ControllerLibrary()

        # Every time we creat a new instance, we will automatically build our UI and populate it
        self.buildUI()
        self.populate()

    def buildUI(self):
        """ This method builds our UI """

        print "Building UI"
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
            action.triggered.connect(lambda: self.delete(item.text()))

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
        print item
        self.library.delete(item)
        self.populate()
        self.popMenu.close()


def showUI():
    """ Return UI dialog"""
    ui = ControllerLibraryUI()
    ui.show()
    return ui
