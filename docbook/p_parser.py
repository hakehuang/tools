#!/usr/bin/python
#usage:
#./p_parser.py <files to be found auto cases>
#e.g.
#./p_parser.py $(ls ../mx50_test_manual/*.xml)

import xml.parsers.expat
import sys
import os
import getopt
import re



Pattern = ['Auto_Level']
Attrib = {
	      'Auto_Level': 'Auto'
#	      'Auto_Level': 'Partially_auto'
		  }
OPattern = "Command_Line"

cflag = 0
pflag = 0
aflag = 0
oflag = 0
cid = ""
skip = 0
startname = []
former_data = ""
cpattern = ""

def start_element(name, attrs):
	global pflag,aflag,oflag,cid,skip,startname
	global Pattern,Attrib,OPattern,cpattern,cflag
	if (pflag == 0 and name.upper() == "TITLE"):
		pflag = 1
		cpattern = ""
		cflag = 0
	if(attrs.has_key('role')):
		if(str(attrs['role']).rstrip().strip() != "Release"):
			skip = 1
			startname.append(name.upper())
			print "add...",startname
	if(name == "sect1"):
		if(attrs.has_key('id')):
			cid = str(attrs['id'])
		if(attrs.has_key('ID')):
			cid = str(attrs['ID'])
		print "ID is ",cid
	if(oflag == 2):
		oflag = 3
def end_element(name):
	global pflag,aflag,oflag,cid,startname,skip,cflag
	global former_data,Pattern,OPattern, Attrib,cpattern
	if(len(former_data)):
		print "former_data",former_data
		if (pflag == 1 and aflag < len(Pattern)):
			for item in Pattern:
				print "item", item
				if(former_data.replace(" ","_").find(item) != -1):
					cflag = 1
					cpattern = item
					print " * find the pattern : " + item
		if (pflag == 0 and cflag > 0):
			item = Attrib[cpattern]
			if(former_data.replace(" ","_").find(item) != -1):
				aflag += 1
				print "* find the attribute: " + item
		elif (pflag == 1 and aflag == len(Attrib)):
			if(former_data.replace(" ","_").find(OPattern) != -1 ):
				print "* find output item: " , former_data
				oflag = 2
	former_data=''
	if (pflag == 1 and name.upper() == "TITLE"):
		pflag = 0
	if(skip == 1 and startname.__contains__(name.upper())):
		startname.remove(name.upper())
		if(len(startname) == 0):
			skip = 0
		print "remaining...",startname
	if(oflag == 4):
		if (skip != 1):
			of.write("\n")
		oflag = 0
		print "output end", name
	if(name == "sect1"):
		cflag = 0
		pflag = 0
		aflag = 0
		oflag = 0
		cid = ""
		cpattern=""
def char_data(data):
	global pflag,aflag,oflag,cid,skip
	global Pattern,Attrib,OPattern,former_data
	sl = len(repr(data))
	string = repr(data)[2:sl-1].replace("\\t","").replace("\\n","")
	former_data = former_data + string
	if (oflag == 3):
		if(skip != 1):
			of.write(cid + "\t")
			of.write(string)
		oflag = 4
		print string
	elif (oflag == 4):
		if(skip != 1):
			of.write(string)
		print string
	else:
		pass

def usage():
	print "-h: this help"
	print "-p <patter name>: the pattern to search e.g. Auto_Level"
	print "-a <attribute>: attribute to match e.g. Auto"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hp:a:o:",\
	["help", "Pattern=\"Auto_Level Priority\"","Attrib=\"Auto P1\"","Output="])
except getopt.error, msg:
	print msg
	print "for help use --help"
	sys.exit(2)

for o,a in opts:
	if o in ("-h", "--help"):
		usage()
		exit(0)
	if o in ("-p", "--Pattern"):
		del Pattern[:]
		Attrib.clear()
		for i in a:
			i = i.replace(" ","")
			if (len(i)):
				Pattern.append(i)
				Attrib[i] = "null"
		print "pattern", Pattern
	if o in ("-a","--Attrib"):
		count = 0
		for i in Attrib.keys():
			temp = a[count].replace(" ","")
			while(len(temp) == 0):
				count += 1
				temp = a[count].replace(" ","")
			Attrib[i] = temp
			count += 1
		print "attribue", Attrib
	if o in ("-o","--Output"):
		OPattern = a

print "process :", args

of = file("exec_table",'w')

# from http://boodebr.org/main/python/all-about-python-and-unicode#UNI_XML
RE_XML_ILLEGAL = u'([\u0000-\u0008\u000b-\u000c\u000e-\u001f\ufffe-\uffff])' + \
                 u'|' + \
                 u'([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % \
                  (unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                   unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff),
                   unichr(0xd800),unichr(0xdbff),unichr(0xdc00),unichr(0xdfff))
regex = re.compile(RE_XML_ILLEGAL)


for filename in args:
		p = xml.parsers.expat.ParserCreate('UTF-8')
		p.StartElementHandler = start_element
		p.EndElementHandler = end_element
		p.CharacterDataHandler = char_data
		try:
			inFile = open(filename,'r')
			print 'inFile is :', filename
			p.ParseFile(inFile)
		finally:
			inFile.close()
		del p

of.close()
