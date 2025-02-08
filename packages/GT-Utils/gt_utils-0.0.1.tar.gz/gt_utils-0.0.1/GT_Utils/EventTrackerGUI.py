from PySide6.QtWidgets import (
	QWidget,
	QApplication,
	QMessageBox,
	QLineEdit,
	QProgressBar,
	QPushButton,
	QHBoxLayout,
	QVBoxLayout,
	QStyle,
	QFileDialog,
)
from PySide6.QtCore import Qt, QStandardPaths, QUrl, QFile, QSaveFile, QDir, QIODevice, Slot
from PySide6.QtWidgets import (QApplication, QComboBox, QDialog, QTabWidget,
								QDialogButtonBox, QGridLayout, QGroupBox, QCheckBox,
								QFormLayout, QHBoxLayout, QLabel, QLineEdit,
								QMenu, QMenuBar, QPushButton, QSpinBox,
								QTextEdit, QVBoxLayout, QWidget, QRadioButton)

import FileUtils.FileUtils as FileUtils
import sys, os, json, shutil, zipfile
from EventTracker.EventTracker import EventTracker
from GUI_Utils.FileSaver import FileSaver
from GUI_Utils.Group.LineEditGroupBox import LineEditGroupBox
from GUI_Utils.Group.GroupBox import GroupBox
from GUI_Utils.Group.ConsoleBox import ConsoleBox
from GUI_Utils.GroupElement.PushButton import PushButton
from GUI_Utils.GroupElement.ComboBox import ComboBox
from GUI_Utils.Window.TabWidget import TabWidget
from GUI_Utils.Window.WidgetForTabWidget import WidgetForTabWidget

class EventTrackerGUI(QDialog):
	def __init__(self):
		super().__init__()
		self.size = [600, 500]
		self.fileSaver = FileSaver("./EventTrackerGUI.json")
		self.tabWidget = TabWidget(self, self.size)
		tab = WidgetForTabWidget()
		self.tabWidget.addTab(tab, "EventTracker")

		self.projectEditBox = LineEditGroupBox(self.fileSaver, "./EventTrackerGUI.json", "选择Event配置文件(.xls)")
		self.projectEditBox.setOpenLineEditGroupBoxAction(self.onOpenLineEditGroupBox)
		tab.addWidget(self.projectEditBox.getQGroupBox())

		tab.addWidget(self.createSdkInfoBox())
		tab.addWidget(self.createEventSdkButtonGroupBox())

		self.consoleBox = ConsoleBox()
		tab.addWidget(self.consoleBox.getQGroupBox())

		self.setFixedSize(self.size[0], self.size[1])
		self.setWindowTitle("GUI Utils")

	def createSdkInfoBox(self):
		sdkInfoGroup = GroupBox("选择配置所需参数")
		sheetNames = []
		xlsPath = self.projectEditBox.editBox.text()
		self.languageChoices = ComboBox(self.fileSaver, "languageIndex", ["csharp", "java"])
		if(FileUtils.getFileExt(xlsPath) == ".xls"):
			selectedLanguageName = self.languageChoices.getSelectComboName()
			self.eventTracker = EventTracker(xlsPath, selectedLanguageName)
			sheetNames = self.eventTracker.sheetNames

		self.sdkChoices = ComboBox(self.fileSaver, "sheetIndex", sheetNames)

		sdkInfoGroup.addWidget(self.sdkChoices.comboBox)
		sdkInfoGroup.addWidget(self.languageChoices.comboBox)
		return sdkInfoGroup.getQGroupBox()

	def onOpenLineEditGroupBox(self, xlsPath):
		self.eventTracker = EventTracker(xlsPath, "csharp")
		sheetNames = self.eventTracker.sheetNames
		for x in range(self.sdkChoices.comboBox.count()):
			self.sdkChoices.comboBox.removeItem(0)
		self.sdkChoices.comboBox.addItems(sheetNames)

	def createEventSdkButtonGroupBox(self):
		sdkGroup = GroupBox("生成埋点相关内容")
		PushButton(sdkGroup, "1.生成埋点方法", self.createFunctions)
		PushButton(sdkGroup, "2.生成埋点声明", self.createEventDeclarations)
		PushButton(sdkGroup, "3.生成埋点统计信息", self.createEventFunctonInfos)
		return sdkGroup.getQGroupBox()

	def createFunctions(self):
		sheetName = self.sdkChoices.comboBox.currentText()
		info = self.eventTracker.createEventFunctions(sheetName)
		self.consoleBox.setLogText(info)

	def createEventDeclarations(self):
		sheetName = self.sdkChoices.comboBox.currentText()
		info = self.eventTracker.createEventDeclarations(sheetName)
		self.consoleBox.setLogText(info)

	def createEventFunctonInfos(self):
		sheetName = self.sdkChoices.comboBox.currentText()
		info = self.eventTracker.createEventFunctonInfos(sheetName)
		self.consoleBox.setLogText(info)

if __name__ == '__main__':
	app = QApplication(sys.argv)
	dialog = EventTrackerGUI()
	sys.exit(dialog.exec())


