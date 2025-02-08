from PySide6.QtWidgets import QWidget, QVBoxLayout
class WidgetForTabWidget():
	def __init__(self, ):
		self.qWidget = QWidget()
		self.layout = QVBoxLayout()
		self.qWidget.setLayout(self.layout)

	def addWidget(self, wiget):
		self.layout.addWidget(wiget)
