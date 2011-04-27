#!/usr/bin/python
#summary the srs map to test cases
#command line
#./xml_sum.py <srs xml file> <directory path where all the cases xml lies>
#e.g.
#./xml_sum.py SRS_release.xml ../mx50_test_manual/
#the result
# the result will be SRS_MAP.xml

import xml.parsers.expat
import sys
import os

path = ''
fn = ''
flag = 0

def start_element(name, attrs):
	global path
	global fn
	global flag
	#print 'Start element:', name, attrs
	if ( name == "testcase"):
		path = ""
		fn = ""
		flag = 0
	elif (name == "title"):
		 flag = 1
	elif (name == "location"):
		flag = 2
	else:
		pass
def end_element(name):
	global path
	global fn
	global flag
	global prefix
	if ( name == "testcase" ):
		path = path.replace("\\","/")
		print  prefix + path + fn
	elif (name == "title"):
		flag = 0
	elif (name == "location"):
		flag = 0
	#print 'End element:', name
def char_data(data):
	global path
	global fn
	global flag
	if (flag == 1 ):
		fn = fn + str(data)
	elif (flag == 2):
		path = path + str(data)
	#print 'Character data:', repr(data)

if len(sys.argv) < 3:
	print "need 2 parameters <xml filename> <output path prefix>"
	sys.exit()

fnSRS = sys.argv[1]
prefix = sys.argv[2]
try:
	fSRS=open(fnSRS,'r')
except:
	print 'can not open', fnSRS
	sys.exit()

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data
p.ParseFile(fSRS)
del p


