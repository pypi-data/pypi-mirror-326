#!/usr/bin/python
# -*-coding: utf-8-*-

import urllib
import re
import os
import xlrd,xlwt
import json
import re
import FileUtils.FileUtils as FileUtils
from EventTracker.EventCreator import EventCreator

class EventTracker(object):
	def __init__(self, eventTrackerXlsFile, languageName):
		self.languageConfigs = configExcels = [{'id': 3, 'languageName': 'java', 'paramConfig': {'string': {'paramName': 'String', 'addParamString': 'putString'}, 'int': {'paramName': 'int', 'addParamString': 'putInt'}, 'float': {'paramName': 'float', 'addParamString': 'putFloat'}, 'bool': {'paramName': 'boolean', 'addParamString': 'putBoolean'}}, 'eventConfig': {'functionDeclarationFormat': 'void Log{0}Event({1});', 'privateFunctionBodyFormat': 'private void Log{0}Event({1}){\n{2}\n}', 'functionBodyFormat': 'public void Log{0}Event({1}){\n{2}\n}', 'eventParamFormat': '{0} {1}', 'eventNameLineFormat': 'var eventName = "{0}";', 'eventParmDictLine': 'Dictionary<string, object> paramDict = new Dictionary<string, object>();', 'eventAddParamFormat': 'paramDict.{1}("{0}", {0});', 'eventTriggerLine': 'LogEvent(eventName, paramDict);', 'eventFirstCallLineFormat': 'if(!IsEventFirstFired("{0}")) Log{1}Event({2});', 'eventCountCallLineFormat': 'if(IsMatchEventCount("{0}", out int matchCount)) Log{1}Event(matchCount);'}}, {'id': 4, 'languageName': 'csharp', 'paramConfig': {'string': {'paramName': 'string', 'addParamString': 'Add'}, 'int': {'paramName': 'int', 'addParamString': 'Add'}, 'float': {'paramName': 'float', 'addParamString': 'Add'}, 'bool': {'paramName': 'bool', 'addParamString': 'Add'}}, 'eventConfig': {'functionDeclarationFormat': 'void Log{0}Event({1});', 'privateFunctionBodyFormat': 'private void Log{0}Event({1}){\n{2}\n}', 'functionBodyFormat': 'public void Log{0}Event({1}){\n{2}\n}', 'eventParamFormat': '{0} {1}', 'eventNameLineFormat': 'var eventName = "{0}";', 'eventParmDictLine': 'Dictionary<string, object> paramDict = new Dictionary<string, object>();', 'eventAddParamFormat': 'paramDict.{1}("{0}", {0});', 'eventTriggerLine': 'LogEvent(eventName, paramDict);', 'eventFirstCallLineFormat': 'if(!IsEventFirstFired("{0}")) Log{1}Event({2});', 'eventCountCallLineFormat': 'if(IsMatchEventCount("{0}", out int matchCount)) Log{1}Event(matchCount);'}}]
		self.languageConfig = [item for item in self.languageConfigs if(item["languageName"] == languageName)][0]
		self.eventTrackerXlsFile = eventTrackerXlsFile
		self.book = xlrd.open_workbook(self.eventTrackerXlsFile);
		self.sheetNames = self.book.sheet_names();

	def createEventFunctions(self, sheetName):
		folder = FileUtils.getFileFolder(self.eventTrackerXlsFile);
		fileName = FileUtils.getFileName(self.eventTrackerXlsFile, False)
		funcList = [];
		sheet = self.book.sheet_by_name(sheetName);
		eventInfoList = self.getEventInfoList(sheet);
		return self.createFunctions(eventInfoList)

	def createEventDeclarations(self, sheetName):
		folder = FileUtils.getFileFolder(self.eventTrackerXlsFile);
		fileName = FileUtils.getFileName(self.eventTrackerXlsFile, False)
		funcList = [];
		sheet = self.book.sheet_by_name(sheetName);
		eventInfoList = self.getEventInfoList(sheet);
		return self.createDeclarations(eventInfoList)

	def createEventFunctonInfos(self, sheetName):
		folder = FileUtils.getFileFolder(self.eventTrackerXlsFile);
		fileName = FileUtils.getFileName(self.eventTrackerXlsFile, False)
		funcList = [];
		sheet = self.book.sheet_by_name(sheetName);
		eventInfoList = self.getEventInfoList(sheet);
		return self.createFunctonInfos(eventInfoList)

	def createFunctonInfos(self, eventInfoList):
		functionBodys = []
		eventCreatorList = [EventCreator(self.languageConfig, item) for item in eventInfoList]
		for eventCreator in eventCreatorList:
			if(eventCreator.isPrivateEvent):
				continue

			eventName = eventCreator.infoDict["eventName"]
			eventInfo = f"{eventName}, {eventName}, 0"
			functionBodys.append(eventInfo)
		eventInfoString = "\n".join(functionBodys)
		return eventInfoString

	def createDeclarations(self, eventInfoList):
		functionBodys = []
		eventCreatorList = [EventCreator(self.languageConfig, item) for item in eventInfoList]
		for eventCreator in eventCreatorList:
			if(eventCreator.isPrivateEvent):
				continue

			eventMainBodyString = eventCreator.getEventDeclarationString()
			functionBodys.append(eventMainBodyString)
		eventInfoString = "\n".join(functionBodys)
		return eventInfoString
		
	def createFunctions(self, eventInfoList):
		print("==> [createFunctions] createFunctions:", len(eventInfoList))
		functionBodys = []
		eventCreatorList = [EventCreator(self.languageConfig, item) for item in eventInfoList]
		for eventCreator in eventCreatorList:
			eventMainBodyString = eventCreator.createFunction(eventCreatorList)
			functionBodys.append(eventMainBodyString)
		eventInfoString = "\n".join(functionBodys)
		return eventInfoString

	def getEventInfoList(self, sheet):
		rowCount = sheet.nrows;
		functionParamArray = [];
		element = {};
		paramTypeColId = 2
		for rowIdx in range(1, rowCount):
			rowValues = sheet.row_values(rowIdx);
			if (not element):
				element["id"] = rowValues[0];
				element["eventName"] = rowValues[1];
				functionParamArray.append(element);
				paramArray = [];
				element["paramArray"] = paramArray;
				if (rowValues[paramTypeColId]):
					param = {};
					param["paramType"] = rowValues[paramTypeColId];
					param["paramName"] = rowValues[paramTypeColId+ 1];
					paramArray.append(param);
			else:
				if (not rowValues[0]):
					paramArray = element["paramArray"];
					if (rowValues[paramTypeColId]):
						param = {};
						param["paramType"] = rowValues[paramTypeColId];
						param["paramName"] = rowValues[paramTypeColId+1];
						paramArray.append(param);
				else:
					element = {};
					element["id"] = rowValues[0];
					element["eventName"] = rowValues[1];
					functionParamArray.append(element);
					paramArray = [];
					element["paramArray"] = paramArray;
					if (rowValues[paramTypeColId]):
						param = {};
						param["paramType"] = rowValues[paramTypeColId];
						param["paramName"] = rowValues[paramTypeColId+1];
						paramArray.append(param);

		return functionParamArray;

# eventTracker = EventTracker("./Excels/EventTracker_Solitaire.xls", "csharp")
# # eventTracker.createEventFunctions("Sheet1")

# # print(eventTracker.createEventFunctions("Sheet1"))
# print(eventTracker.createEventDeclarations("Sheet1"))
# # eventTracker.createEventDeclarations()








