from PySide6.QtWidgets import QComboBox

class ComboBox():
	def __init__(self, fileSaver, savedToKey, comboNames):
		self.fileSaver = fileSaver
		self.savedToKey = savedToKey
		self.comboNames = comboNames
		self.comboBox = QComboBox()
		self.comboBox.addItems(comboNames)
		self.comboBox.currentIndexChanged.connect(lambda value: self.fileSaver.setInfo(self.savedToKey, value))
		self.comboBox.setCurrentIndex(self.fileSaver.getInfo(self.savedToKey, 0))

	def getSelectIndex(self):
		selectedIndex = self.fileSaver.getInfo(self.savedToKey, 0)
		return selectedIndex

	def getSelectComboName(self):
		selectedIndex = self.fileSaver.getInfo(self.savedToKey, 0)
		lanIndex = self.getSelectIndex()
		selectedComboName = self.comboNames[selectedIndex]
		return selectedComboName