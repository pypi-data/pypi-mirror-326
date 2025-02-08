from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QStyle, QFileDialog
from GUI_Utils.Group.GroupBox import GroupBox

class LineEditGroupBox():
	def __init__(self, fileSaver, savedToKey, xlsDescInfo):
		self.fileSaver = fileSaver
		self.savedToKey = savedToKey
		self.editBox = QLineEdit()
		self.lineEditGroup = GroupBox(xlsDescInfo)
		self.editBox.setText(self.fileSaver.getInfo(self.savedToKey, "C:/Users/Administrator/Desktop"))
		self.lineEditGroup.addWidget(self.editBox)
		openFolderAction = self.editBox.addAction(qApp.style().standardIcon(QStyle.SP_DirOpenIcon), QLineEdit.TrailingPosition)
		openFolderAction.triggered.connect(lambda: self.onOpenFolder())

	def setOpenLineEditGroupBoxAction(self, openAction):
		self.openAction = openAction

	def onOpenFolder(self):
		dirInfos =  QFileDialog.getOpenFileName(parent = None, caption = '请选择xls文件', dir = self.editBox.text(),filter = 'file(*.xls)')
		if dirInfos:
			xlsPath = dirInfos[0]
			self.fileSaver.setInfo(self.savedToKey, xlsPath)
			self.editBox.setText(xlsPath)
			self.openAction(xlsPath)

	def getQGroupBox(self):
		return self.lineEditGroup.groupBox