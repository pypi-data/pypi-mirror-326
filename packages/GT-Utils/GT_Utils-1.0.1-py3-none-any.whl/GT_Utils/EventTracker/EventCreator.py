#!/usr/bin/python
# -*-coding: utf-8-*-

import urllib
import re
import os
import xlrd,xlwt
import json
import re
import GT_Utils.FileUtils.FileUtils as FileUtils

class EventCreator(object):
	def __init__(self, config, infoDict):
		self.config = config;
		self.infoDict = infoDict;
		self.isPrivateEvent = ("_count" in self.infoDict["eventName"]) or ("_first" in self.infoDict["eventName"])


	def createFunction(self, eventCreatorList):
		eventName = self.infoDict["eventName"]
		paramArray = self.infoDict["paramArray"]
		eventCapitalName = self.getEventCapitalName(eventName)

		eventParamString = self.getEventParamString(paramArray)
		eventFunctionBodyString = self.getEventFunctionBodyString(eventName, paramArray)

		eventMainBodyString = self.config["eventConfig"]["functionBodyFormat"] if(not self.isPrivateEvent) else self.config["eventConfig"]["privateFunctionBodyFormat"]
		eventMainBodyString = self.formatString(eventMainBodyString, 0, eventCapitalName)
		eventMainBodyString = self.formatString(eventMainBodyString, 1, eventParamString)
		eventMainBodyString = self.formatString(eventMainBodyString, 2, eventFunctionBodyString)

		firtFireEventCreator = self.getEventInfoFirstFire(eventName, eventCreatorList)
		countEventCreator = self.getEventInfoCount(eventName, eventCreatorList)

		if(firtFireEventCreator != None):
			eventMainBodyString = self.insertString(eventMainBodyString, firtFireEventCreator.getFirstFireCallString())
		if(countEventCreator != None):
			eventMainBodyString = self.insertString(eventMainBodyString, countEventCreator.getCountCallString())

		return eventMainBodyString;

	def insertString(self, info, insertString):
		lines = info.split("\n")
		insertLines =  insertString.split("\n")
		insertLines = [("\t" + item) for item in insertLines]
		startLines = lines[0:-1]
		endLines = lines[-1:]

		newLines = startLines + insertLines + endLines

		newInfo = "\n".join(newLines)
		return newInfo

	def getFirstFireCallString(self):
		eventName = self.infoDict["eventName"]
		paramArray = self.infoDict["paramArray"]
		funcCallFormat = self.config["eventConfig"]["eventFirstCallLineFormat"]
		eventCapitalName = self.getEventCapitalName(eventName)
		paramNames = [item["paramName"] for item in paramArray]
		paramNamesString = ", ".join(paramNames);

		eventFunctionCallString = funcCallFormat;
		eventFunctionCallString = self.formatString(eventFunctionCallString, 0, eventName)
		eventFunctionCallString = self.formatString(eventFunctionCallString, 1, eventCapitalName)
		eventFunctionCallString = self.formatString(eventFunctionCallString, 2, paramNamesString)
		return eventFunctionCallString; 

	def getCountCallString(self):
		eventName = self.infoDict["eventName"]
		paramArray = self.infoDict["paramArray"]
		funcCallFormat = self.config["eventConfig"]["eventCountCallLineFormat"]
		eventCapitalName = self.getEventCapitalName(eventName)
		paramNames = [item["paramName"] for item in paramArray]
		paramNamesString = ", ".join(paramNames);

		eventFunctionCallString = funcCallFormat;
		eventFunctionCallString = self.formatString(eventFunctionCallString, 0, eventName)
		eventFunctionCallString = self.formatString(eventFunctionCallString, 1, eventCapitalName)
		eventFunctionCallString = self.formatString(eventFunctionCallString, 2, paramNamesString)
		return eventFunctionCallString; 

	def getEventDeclarationString(self):
		eventName = self.infoDict["eventName"]
		paramArray = self.infoDict["paramArray"]
		funcCallFormat = self.config["eventConfig"]["functionDeclarationFormat"]
		eventCapitalName = self.getEventCapitalName(eventName)
		eventParamString = self.getEventParamString(paramArray)

		eventFunctionCallString = funcCallFormat;
		eventFunctionCallString = self.formatString(eventFunctionCallString, 0, eventCapitalName)
		eventFunctionCallString = self.formatString(eventFunctionCallString, 1, eventParamString)
		return eventFunctionCallString; 

	def getEventCapitalName(self, eventName):
		return "".join([item.capitalize() for item in eventName.split("_")])

	def getEventFunctionBodyString(self, eventName, paramArray):
		eventFunctionBody = []
		eventNameLine = self.formatString(self.config["eventConfig"]["eventNameLineFormat"], 0, eventName)
		eventParmDictLine = self.config["eventConfig"]["eventParmDictLine"]
		eventTriggerLine = self.config["eventConfig"]["eventTriggerLine"]

		eventFunctionBody.append(eventNameLine)
		eventFunctionBody.append(eventParmDictLine)

		for paramInfo in paramArray:
			paramType = paramInfo["paramType"]
			paramName = paramInfo["paramName"]
			addParamString = self.config["paramConfig"][paramType]["addParamString"]
			eventAddParamLine = self.formatString(self.config["eventConfig"]["eventAddParamFormat"], 0, paramName)
			eventAddParamLine = self.formatString(eventAddParamLine, 1, addParamString)
			eventFunctionBody.append(eventAddParamLine)

		eventFunctionBody.append(eventTriggerLine)
		eventFunctionBodyString = "\t" + "\n\t".join(eventFunctionBody)

		return eventFunctionBodyString

	def getEventParamString(self, paramArray):
		paramBody = []
		for paramInfo in paramArray:
			paramType = paramInfo["paramType"]
			paramName = paramInfo["paramName"]
			typeString = self.config["paramConfig"][paramType]["paramName"]
			eventAddParamLine = self.formatString(self.config["eventConfig"]["eventParamFormat"], 0, typeString)
			eventAddParamLine = self.formatString(eventAddParamLine, 1, paramName)
			paramBody.append(eventAddParamLine)
		return ", ".join(paramBody)

	def formatString(self, formatInfo, paramId, paramInfo):
		placeHolder = "{{{}}}".format(paramId)
		result = formatInfo.replace(placeHolder, paramInfo)
		return result

	def getEventInfoFirstFire(self, eventName, eventInfoList):
		eventFirstFireName = f"{eventName}_first"
		eventInfos = [item for item in eventInfoList if(item.infoDict["eventName"] == eventFirstFireName)]
		if(len(eventInfos) > 0):
			return eventInfos[0];
		else:
			return None

	def getEventInfoCount(self, eventName, eventInfoList):
		eventFirstFireName = f"{eventName}_count"
		eventInfos = [item for item in eventInfoList if(item.infoDict["eventName"] == eventFirstFireName)]
		if(len(eventInfos) > 0):
			return eventInfos[0];
		else:
			return None


