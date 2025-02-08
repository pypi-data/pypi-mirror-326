from PySide6.QtWidgets import QPushButton
class PushButton():
	def __init__(self, groupBox, actionName, action):
		self.qButton = QPushButton(actionName)
		self.qButton.clicked.connect(action)
		groupBox.layout.addWidget(self.qButton)