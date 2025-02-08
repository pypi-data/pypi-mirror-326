from PySide6.QtWidgets import QTabWidget,QVBoxLayout

class TabWidget():
	def __init__(self, window, size):
		self.tabWidget = QTabWidget(window)
		self.layout = QVBoxLayout()
		self.tabWidget.setLayout(self.layout)
		self.tabWidget.setGeometry(0, 0, size[0], size[1])

	def addTab(self, tab, tabName):
		self.tabWidget.addTab(tab.qWidget, tabName)
		