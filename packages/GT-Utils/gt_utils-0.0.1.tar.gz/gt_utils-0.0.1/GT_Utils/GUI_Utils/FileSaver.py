import sys
import FileUtils.FileUtils as FileUtils
import os, json, shutil, zipfile

class FileSaver():
	def __init__(self, savedToFile):
		self.savedToFile = savedToFile

	def setInfo(self, infoKey, infoValue):
		if(not os.path.exists(self.savedToFile)):
			FileUtils.writeFile(self.savedToFile, json.dumps({}));

		infoString = FileUtils.readFile(self.savedToFile)
		infoDict = json.loads(infoString)
		infoDict[infoKey] = infoValue;
		FileUtils.writeFile(self.savedToFile, json.dumps(infoDict, indent = 4));

	def getInfo(self, infoKey, defaultValue):
		if(not os.path.exists(self.savedToFile)):
			FileUtils.writeFile(self.savedToFile, json.dumps({}));

		infoString = FileUtils.readFile(self.savedToFile)
		infoDict = json.loads(infoString)
		if(infoKey not in infoDict):
			return defaultValue;
		return infoDict[infoKey]