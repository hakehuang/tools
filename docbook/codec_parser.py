#!/usr/bin/python
#summary the srs map to test cases
#command line
#./codec_parser.py <xml file> <directory prefix you want to add>
#e.g.
#./codec_parser.py P1.xml /mnt/nfs
#the result
# the result will output in console

import xml.parsers.expat
import sys
import os
import string

path = ''
fn = ''
flag = 0
cnt = 1

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
	global cnt
	if ( name == "testcase" ):
		path = path.replace("\\","/")
		print   "File" + str(cnt) + "=file://" + prefix + path + fn
		cnt = cnt + 1
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

cmds = "cat " + fnSRS + " | grep testcase | wc -l" 

numbs = os.popen(cmds).read()

print "[playlist]"
#print numbs
print "NumberOfEntries=" + str(int(numbs) / 2)

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data
p.ParseFile(fSRS)
del p


