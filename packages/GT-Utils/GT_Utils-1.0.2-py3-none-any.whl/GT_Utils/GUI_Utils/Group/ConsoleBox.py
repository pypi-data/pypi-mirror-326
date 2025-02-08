from PySide6.QtWidgets import QTextEdit

class ConsoleBox():
	def __init__(self):
		self.qTextEdit = QTextEdit()

	def setLogText(self, info):
		self.qTextEdit.setPlainText("");
		self.qTextEdit.append(info)

	def getQGroupBox(self):
		return self.qTextEdit