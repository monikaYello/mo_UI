'''
This creates the Maya version of PyQt Desing .py file
Connects buttons to functions



'''

from PySide import QtCore, QtGui
import PyQt.bulletUI as customUI
from shiboken import wrapInstance
import maya.OpenMayaUI as omui
import mo_Dynamics.bulletTool as bulletTool


def maya_main_window():
	main_window_ptr = omui.MQtUtil.mainWindow()
	return wrapInstance(long(main_window_ptr), QtGui.QWidget)

class ControlMainWindow(QtGui.QDialog):

	def __init__(self, parent=None):

		super(ControlMainWindow, self).__init__(parent)
		self.setWindowFlags(QtCore.Qt.Tool)
		self.ui = customUI.Ui_Dialog()
		self.ui.setupUi(self)

		self.ui.create_rigid_btn.clicked.connect(bulletTool.createRigidiBody())
		self.ui.create_rigid_btn.clicked.connect(self.cn)

	def connectRiggCtrlsAndBakeWin(self):
		print 'Hello {0} !'
		bulletTool.connectRiggCtrlsAndBake(replaceRegex=['_grp_bullet', 'Grp_ctrl'], bulletStartFrame=None, bulletSolverNode='bulletSolverShape1')


myWin = ControlMainWindow(parent=maya_main_window())
myWin.show()
