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

temptag = ""
caseNM = "" 
startc = 0
cur_SRS = ""
cur_map_list = []

def start_case(name,attrs):
	global temptag
	global caseNM
	global cur_SRS
	global cur_map_list
	global startc
	#print 'Start element:', name, attrs
	if(attrs.has_key('id') or attrs.has_key('ID')):
		if(attrs.has_key('id')):
			caseNM = str(attrs['id'])
		else:
			caseNM = str(attrs['ID'])
		startc = 1
		temptag = name
	elif(startc == 1 and name == "sect3" and attrs.has_key('condition')):
		srs_id = str(attrs['condition'])
		print "searching.. ", cur_SRS ,srs_id
		if(str(srs_id).strip().find(str(cur_SRS).strip()) != -1):
			print 'caseNM cur_SRS', caseNM, cur_SRS
			cur_map_list.append(caseNM)
		else:
			pass
	else:
		pass
def end_case(name):
	global temptag
	global caseNM
	global cur_SRS
	global startc
	if(temptag == name and startc == 1):
		temptag = ""
		startc = 0
		caseNM = ""
def search_caseID(srs, fxml):
	global cur_SRS
	print 'secarhing id', srs
	pc = xml.parsers.expat.ParserCreate()
	pc.StartElementHandler = start_case
	pc.EndElementHandler = end_case
	cur_SRS = srs
	try:
		tFile = open(fxml,'r')
		pc.ParseFile(tFile)
	finally:
		tFile.close()
		del pc

def search_SRS(id):
	global cur_map_list
	global fm
	global spath
	if (os.path.isdir(spath)):
		for i in os.listdir(spath):
			print 'searching in', spath+i
			if (os.path.isfile(spath+i)):
				if(i.find(".xml") != -1):
					search_caseID(id,spath + i)
		if(len(cur_map_list)):
			fm.write("<sect1><title>")
			fm.write(str(id) + " is mapped to below case(s)")
			fm.write("</title>")
			for item in cur_map_list:
				fm.write("<section><para>\n")
				fm.write(item)
				fm.write("\n</para></section>")
			fm.write("</sect1>")
		else:
			fm.write("<sect1><title>")
			fm.write(str(id))
			fm.write("</title>")
			fm.write("<section><title>\n")
			fm.write("No cases mapped or not testable!")
			fm.write("\n</title></section>")
			fm.write("</sect1>")
		del cur_map_list[:]			
# 3 handler functions
def start_element(name, attrs):
#	print 'Start element:', name, attrs
	if(attrs.has_key('name')):
		srsID = str(attrs['name'])
		print 'find SRS id',srsID
		search_SRS(srsID) 	
def end_element(name):
	pass
	#print 'End element:', name
def char_data(data):
	pass
	#print 'Character data:', repr(data)

if len(sys.argv) < 2:
	print 'need 2 parameter 1 SRS.xml, 2 direct to search SRS'
	sys.exit()
#first open SRS file
fnSRS = sys.argv[1]
spath = sys.argv[2]
try:
	fSRS=open(fnSRS,'r')
except:
	print 'can not open', fnSRS
	sys.exit()
try:
	fm= open("SRS_MAP.xml",'w')
except:
	print 'can not create SRS_MAP.xml'
	sys.exit()

fm.write("<?xml-stylesheet type=\"text/xsl\" href=\"srs.xsl\"?>\n")
fm.write("<chapter>\n")
fm.write("<title>srs to case mapping</title>\n")

p = xml.parsers.expat.ParserCreate()
p.StartElementHandler = start_element
p.EndElementHandler = end_element
p.CharacterDataHandler = char_data
p.ParseFile(fSRS)
del p

fm.write("\n</chapter>")
fm.close()


