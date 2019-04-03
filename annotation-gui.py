"""
	Annotater Driver for Annotation task.
	Objective: To annotate the phrases in 'Source*.csv'
"""
print ("Annotation - GUI")

import csv
import sys
import json
import subprocess

from os import mkdir
from os import listdir
from os.path import isfile, join
from datetime import datetime
from ast import literal_eval as le

# LOGGER FUNCTION
def writeLog(writeData : str):
	with open("Logger.txt", 'a') as FLog:
		FLog.write("\n"+str(datetime.datetime.now())+"\t"+writeData.upper())

writeLog("\n\nBEGIN SESSION")

# CREATE SOURCEEDITABLE.CSV IF IT DOESN'T EXIST
def makeSourceEditable():
	writeLog("BEGIN: MAKE SOURCEEDITABLE")
	
	tempFileNameHolder = ''
	
	for fileName in filesInDir:
		if "source" in fileName.lower():
			try:
				writeLog("PRESUMING LINUX/MACOS... TRYING CP")
				subprocess.run(['cp', fileName, 'SourceEditable.csv'], shell=True)
				writeLog("FOUND AND COPIED SOURCE TO SOURCEEDITABLE")
			except:
				pass	

			writeLog("PRESUMING WINDOWS... SHIFTING FROM CP TO COPY")

			try:
				subprocess.run(['copy', fileName, 'SourceEditable.csv'], shell=True)
				writeLog("FOUND AND COPIED SOURCE TO SOURCEEDITABLE")
			except:
				writeLog("COPY SOURCE TO SOURCEEDITABLE: FAILED! ASKING FOR MANUAL COPY & RENAME")
				
				print ("There was an error with the Program. For the program to run, please:\n\n1. Create a copy of:\t"+fileName+"\n2. Rename the Copy to:\t SourceEditable.csv\n\nHit Enter")
				
				understandInput = input()
				if understandInput == '\n':
					writeLog("INPUT RECEIVED UNDERSTANDINPUT:\tENTER")
				else:
					writeLog("INPUT RECEIVED UNDERSTANDINPUT:\t" + understandInput)
				
				writeLog("SYS EXIT")
				sys.exit()
			
			tempFileNameHolder = fileName

	writeLog("COMPLETE: MAKE SOURCEEDITABLE")
	
	return tempFileNameHolder

# ORIGINAL FILE NAME: SOURCE*.CSV
fileNameOrigSource = ''

# FIND ALL THE FILES IN THE CURRENT DIRECTORY
filesInDir = [f for f in listdir('.') if isfile(join('.', f))]

# LOOK/CREATE SOURCEEDITABLE.CSV
writeLog("LOOKING FOR SOURCEEDITABLE.CSV")
if "SourceEditable.csv" not in filesInDir:
	fileNameOrigSource = makeSourceEditable()
writeLog("FOUND/COMPLETED: SOURCEEDITABLE")

# METADATA STRUCTURE
metaData = {
	"Sessions_Activated" : 0,
	"OriginalSourceFileName": None,
	"WordsCompleted" : 0,
	"Names" : []
}

# LOOK/CREATE METADATA_ANNOTATION.JSON
writeLog("LOOKING FOR METADATA_ANNOTATION.JSON")
if "metadata_annotation.json" in filesInDir:
	with open("metadata_annotation.json", 'r') as Fobj:
		rawMetaData = Fobj.read()
		metaData = json.loads(rawMetaData)
		
		writeLog("METADATA_ANNOTATION.JSON LOADED")
	
else:
	writeLog("METADATA_ANNOTATION.JSON NOT FOUND")
	writeLog("CREATING METADATA_ANNOTATION.JSON")

	metaData["OriginalSourceFileName"] = fileNameOrigSource

	writeLog("CREATED METADATA_ANNOTATION.JSON")

# LOOK/CREATE SOURCEALTS/ OR SOURCEALTS\
writeLog("CREATE/LOOK FOR SOURCEALTS DIR")
try:
	mkdir("SourceAlts")
	writeLog("CREATED SOURCEALTS")
except:
	writeLog("LOCATED SOURCEALTS")

# GET NAME
print ("Welcome!")

print ("Please Enter Your Name:\t")
name = str(input())

writeLog("NAME:\t"+name)

# IMPORT NLTK ATTEMPT#1
try:
	import nltk
	writeLog("NLTK#1 IMPORTED")
except:
	try:
		subprocess.run(['pip', 'install', 'nltk']) # PIP INSTALL (PIP3 DOESN'T EXIST)
		writeLog("PIP INSTALL NLTK: SUCCESS")
	except:
		subprocess.run(['pip3', 'install', 'nltk']) # PIP3 INSTALL (PIP DOESN'T EXIST)
		writeLog("PIP3 INSTALL NLTK: SUCCESS")

# IMPORT NLTK ATTEMPT#2
try:
	import nltk
	writeLog("NLTK#2 IMPORTED")
except:
	print ("ERROR1: NLTK\n\nEXIT")
	writeLog("IMPORT NLTK: FAIL! SYS EXIT")
	sys.exit()

# IMPORT PYGAME ATTEMPT#1
try:
	import pygame as pg
	writeLog("PYGAME#1 IMPORTED")
except:
	try:
		subprocess.run(['pip', 'install', 'pygame']) # PIP INSTALL (PIP3 DOESN'T EXIST)
		writeLog("PIP INSTALL PYGAME: SUCCESS")
	except:
		subprocess.run(['pip3', 'install', 'pygame']) # PIP3 INSTALL (PIP DOESN'T EXIST)
		writeLog("PIP3 INSTALL PYGAME: SUCCESS")

# IMPORT PYGAME ATTEMPT#2
try:
	import pygame as pg
	writeLog("PYGAME#2 IMPORTED")
except:
	print ("ERROR1: PYGAME\n\nEXIT")
	writeLog("IMPORT PYGAME: FAIL! SYS EXIT")
	sys.exit()

# ATTEMPT TO DOWNLOAD NLTK.WORDNET
try:
	nltk.download('wordnet')
except:
	print ("ERROR2: NLTK - DOWNLOAD\n\nEXIT")
	writeLog("DOWNLOAD NLTK.DOWNLOAD('WORDNET'): FAIL! SYS EXIT")
	sys.exit()

from nltk.corpus import wordnet

globalSynonymsList = []

try:
	writeLog("TRY READING SOURCEEDITABLE")
	with open("SourceEditable.csv", 'r') as Fobj:
		reader = csv.reader(Fobj)

		for row in reader:
			globalSynonymsList.append((row[0], row[1], row[2]))
	writeLog("SUCCESS READING SOURCEEDITABLE")
except:
	try:
		writeLog("TRY READING SOURCE")
		with open(fileNameOrigSource, 'r') as Fobj:
			reader = csv.reader(Fobj)

			for row in reader:
				globalSynonymsList.append((row[0], row[1], row[2]))
		writeLog("SUCCESS READING SOURCE")
	except:
		print ("ERROR3: READING SOURCE FILE\n\nEXIT")
	
		writeLog("READING SOURCE FILE: FAIL! SYS EXIT")
		sys.exit()

synonymsTotal = [] 
relSynonyms = []