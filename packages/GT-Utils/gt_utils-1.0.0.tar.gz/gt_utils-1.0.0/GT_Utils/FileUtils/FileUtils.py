#!/usr/bin/python
# -*-coding: utf-8-*-

import urllib
import re
import os
import json
import re
import io
import platform
import pandas as pd
import struct
import shutil

def checkCreateFolder(folder):
	if(not os.path.exists(folder)):
		os.makedirs(folder);

def moveFile(src, dest):
	checkCreateFolder(dest)
	shutil.move(src, dest)

def copyFile(srcFile, targetFile):
	targetFileFolder = getFileFolder(targetFile)
	if not os.path.exists(targetFileFolder):
		os.makedirs(targetFileFolder)
	shutil.copyfile(srcFile, targetFile)

def writeFile(fileName, info):
	checkCreateFolder(getFileFolder(fileName))
	with io.open(fileName, "w", encoding="utf-8") as my_file:
		my_file.write(info)

def readFile(fileName):
	data = "null"
	with io.open(fileName, "r", encoding="utf-8") as myFile:
		data = myFile.read()
	return data;

def readConfigExcel(configExcel, parsedKeys = []):
	# print("==> readConfigExcel:", configExcel)
	df1 = pd.read_excel(configExcel, index_col = 0).ffill()
	jsonStr = df1.to_json(orient="records", force_ascii=False)
	tmpConfigs = json.loads(jsonStr)
	for item in tmpConfigs:
		for key in item:
			if(key in parsedKeys):
				item[key] = json.loads(item[key])
	return tmpConfigs

def writeConfigExcel(configExcel, jsonArray):
	dataFrame = pd.DataFrame(jsonArray)
	dataFrame.to_excel(configExcel, encoding='utf-8', index=True, header=True)

def getTopFiles(folder, exts = ""):
	allFiles = getAllFiles(folder, exts)
	topFiles = [item for item in allFiles if(isFileInFolder(item, folder))]
	
	return topFiles

def getAllFiles(folder, exts = ""):
	fileList = []
	for root,folders, files in os.walk(folder):
		isCurrentFolder = os.path.normcase(folder) == os.path.normcase(root)
		fullPathFiles = [os.path.join(root,item) for item in files]
		fileList.extend(fullPathFiles)

	fileList = [item for item in fileList if(isFileWithExts(item, exts))]
	return fileList

def isFileInFolder(file, topFolder):
	fileFolder = getFileFolder(file)
	isCurrentFolder = os.path.normcase(fileFolder) == os.path.normcase(topFolder)
	return isCurrentFolder

def isFileWithExts(file, exts = ""):
	extList = exts.split(";")
	fileExt = getFileExt(file)

	# print(f"file: {file}, extList:{extList}, fileExt:{fileExt}")
	isWithExts = (exts == "") or (fileExt in extList)
	return isWithExts

def getFileFolder(file):
	fsList = get_filePath_fileName_fileExt(file)
	return fsList[0]

def getFileName(file, hasExt = False):
	fsList = get_filePath_fileName_fileExt(file)
	if (hasExt):
		return "{}{}".format(fsList[1], fsList[2])
	else:
		return fsList[1]

def getFileExt(file, hasExt = False):
	fsList = get_filePath_fileName_fileExt(file)
	return fsList[2]

def get_filePath_fileName_fileExt(filename):
	(filepath,tempfilename) = os.path.split(filename);
	(shotname,extension) = os.path.splitext(tempfilename);
	return filepath,shotname,extension;

def readInt(datFile, offset):
	allBytes = readBytes(datFile)
	dateBytes = allBytes[offset:offset+4]
	ret = struct.unpack("i", dateBytes)[0]
	return ret

def readBytes(datFile):
	file = open(datFile, "rb")
	allBytes = file.read()
	file.close()
	return allBytes

def writeBytes(datFile, allBytes):
	checkCreateFolder(getFileFolder(datFile))
	if(type(allBytes) == list):
		allBytes = bytearray(allBytes)
	file = open(datFile, "wb")
	file.write(allBytes)
	file.close()