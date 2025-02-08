from PySide6.QtWidgets import QGroupBox, QHBoxLayout
class GroupBox():
	def __init__(self, groupDesc):
		self.groupBox = QGroupBox(groupDesc)
		self.layout = QHBoxLayout()
		self.groupBox.setLayout(self.layout)
		
	def addWidget(self, widget):
		self.layout.addWidget(widget)

	def getQGroupBox(self):
		return self.groupBox
