#!/usr/bin/python
#usage:
#./p_parser.py <files to be found auto cases>
#e.g.
#./p_parser.py $(ls ../mx50_test_manual/*.xml)

import xml.parsers.expat
import sys
import os
import getopt

Pattern = "Auto_Level"
Attrib = "Auto"
OPattern = "Command Line"

pflag = 0
aflag = 0
oflag = 0
cid = ""

def start_element(name, attrs):
	global pflag,aflag,oflag,cid
	global Pattern,attrib,OPattern
	if (pflag == 0 and name.upper() == "TITLE"):
		pflag = 1
	if(name == "sect1"):
		if(attrs.has_key('id')):
			cid = str(attrs['id'])
		if(attrs.has_key('ID')):
			cid = str(attrs['ID'])
	if(oflag == 2):
		oflag = 3
def end_element(name):
	global pflag,aflag,oflag,cid
	if (pflag == 1 and name.upper() == "TITLE"):
		pflag = 0
	if (aflag == 1 and name.upper() == "FORMALPARA"):
		aflag = 0
	if(oflag == 4):
		of.write("\n")
		oflag = 0
		print "output end", name
	if(name == "sect1"): 
		pflag = 0
		aflag = 0
		oflag = 0
		cid = ""
def char_data(data):
	global pflag,aflag,oflag,cid
	global Pattern,attrib,OPattern
	sl = len(repr(data))
	string = repr(data)[2:sl-1].replace("\\t","").replace("\\n","")
	if (pflag == 1 and oflag == 0):
		if(string.find(Pattern) != -1):
			aflag = 1
	elif (aflag == 1):
		if(string.find(Attrib) != -1):
			oflag = 1
			#print 'oflag Character data', string
	elif (oflag == 1):
		if(string == OPattern ):
			oflag = 2
		#print 'oflag 2 Character data', string
	elif (oflag == 3):
		of.write(cid + "\t")
		of.write(string)
		oflag = 4
		print string
	elif (oflag == 4):
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
	["help", "Pattern=","Attrib=","Output="])
except getopt.error, msg:
	print msg
	print "for help use --help"
	sys.exit(2)

for o,a in opts:
	if o in ("-h", "--help"):
		usage()
		exit(0)
	if o in ("-p", "--Pattern"):
		Pattern = a
	if o in ("-a","--Attrib"):
		Attrib = a
	if o in ("-o","--Output"):
		OPattern = a

print "process :", args

of = file("exec_table",'w')

for filename in args:
		p = xml.parsers.expat.ParserCreate()
		p.StartElementHandler = start_element
		p.EndElementHandler = end_element
		p.CharacterDataHandler = char_data
		fp = [ ]
		fp = os.path.split(filename) 
		fname = "P_" + fp[1]
		f = file(fname, 'w')
		f.write("<sheet>")
		try:
			inFile = open(filename,'r')
			print 'inFile is :', filename
			p.ParseFile(inFile)
		finally:
			inFile.close()
			f.write("</sheet>")
			f.close
		del p

of.close()
