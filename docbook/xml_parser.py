#!/usr/bin/python
#./xml_parser.py $(ls ../mx50_test_manual/*.xml)

import xml.parsers.expat
import sys
import os
import time

#virables
ori_array = [ ]
ori_end_array = [ ]
target_array = [ ]
target_array_attr = [ ]
target_end_array = [ ]
sa = [ ]
seq = 0
seq_end = 0
add_content = 0
pat = -1
cnt = 0
module = ""
cid = ""
multi_line = 0

def init_data():
	global seq, seq_end, add_content, pat, cnt, module,cid,multi_line 
	seq = 0
	seq_end = 0
	add_content = 0
	pat = -1
	cnt = 0
	module = ""
	cid = ""
	multi_line = 0
# 3 store the  
def store_ori_start_element(name, attrs):
	ori_array.append(name)
def store_ori_end_element(name):
	ori_end_array.append(name)
def store_target_start_element(name, attrs):
	target_array.append(name)
	if(len(attrs)):
		target_array_attr.append(attrs)
	else:
		target_array_attr.append({'NA':'NA'})
def store_target_end_element(name):
	target_end_array.append(name)
# 3 handler functions
def start_element(name, attrs):
	global add_content
	global seq
	global len_ori
	global ori_array
	global target_array
	global f
	global sa
	global cnt
	global module
	global cid
	global multi_line
	print 'Start element:', name, attrs, seq, len_ori
	if(name == "screen"):
		multi_line = 1
	if (seq < len_ori and name == ori_array[seq]):
		if( "skip" == target_array[seq]):
			add_content = 0
		elif ("char" == target_array[seq]):
			add_content = 1
			f.write("\n")
		else:
			f.write("\n<")
			f.write(target_array[seq])
			key = target_array_attr[seq].keys()[0]
			value = target_array_attr[seq].values()[0]
			if(key != "NA"):
				f.write(" " + str(key) + "=\"" + str(value) + "\"");
			if(seq == 0):
			  	f.write(" id=")
				f.write("\""+str(cnt)+"\"")
				f.write(">")
				if(attrs.has_key('id')):
					f.write("\n<field name=\"Test Case ID\">" + str(attrs['id'])  +"</field>")
					cid = str(attrs['id'])
				elif(attrs.has_key('ID')):
					f.write("\n<field name=\"Test Case ID\">" + str(attrs['ID'])  +"</field>")
					cid = str(attrs['ID'])
				#add additional informations
				f.write("\n<field name=\"Platform : OS\">" + "MX50_EVK:Linux" + "</field>")
				f.write("\n<field name=\"Type\">" + "Linux BSP" + "</field>")
				f.write("\n<field name=\"Module\">" + module + "</field>")
				f.write("\n<field name=\"Test Point\">" + "default test point for " + module + "</field>")
				f.write("\n<field name=\"Source\">" + "FSL MAD" + "</field>")
				f.write("\n<field name=\"Owner\">" + "Hake Huang" + "</field>")
				cnt = cnt + 1
			else:
				f.write(">")
			add_content = 1
		seq = seq + 1
	else:
		#abnormal happen
		add_content = 0
		if(seq > 0 and seq < len_ori - 1):
			print 'abnormal!!!', name, ori_array[seq],seq
			#try to use the parent attribute
			if(len(sa)):
				add_content = sa[-1]
		elif(seq == 0):
			if(name == "chapter" and attrs.has_key('name')):
				module=str(attrs['name'])
			else:
				pass
		else:
			pass
		#in this cases the content seems need
	sa.append(add_content)
	return
def end_element(name):
	global add_content
	global seq_end
	global seq
	global ori_end_array
	global target_end_array
	global f
	global sa
	global pat
	global multi_line
	print 'End element:', name, seq_end, len(ori_end_array)
	if(name == "screen"):
		multi_line = 0
	if (name == ori_end_array[seq_end] and seq > 0):
		if(target_end_array[seq_end] == "char" ):
			pass
		elif("skip" == target_end_array[seq_end]):
			pass
		else:
			if (pat != -1):
		  		f.write("]]>")
				pat = -1
			f.write("\n</")
			f.write(target_end_array[seq_end])
			f.write(">")
		seq_end = seq_end + 1
		if (seq_end >= len(ori_end_array)):
			seq_end = 0
			seq = 0
	else:
		pass
		#abnormal happen
		print 'end abnormal!!!', name , ori_end_array[seq_end], seq_end
	sa.pop()
	return
def char_data(data):
	global add_content
	global seq
	global ori_array
	global target_array
	global f
	global pat
	global cid
	global multi_line
	if(data == '\n'):  
		return  
	if(data.isspace()):  
		return  
	print 'Character data:', repr(data)
	temp = repr(data)
	temp = temp.replace(cid + ":","");
	#temp = temp.replace(":","");
	tl = len(temp)
	if(add_content == 1):
		if (pat == -1):
			pat1 = temp.find("&")
			pat2 = temp.find("<")
			if (pat1 != -1 or pat2 != -1):
		  		f.write("<![CDATA[")
				pat = 0
		temp = temp[2:tl-1].replace("\\t","")
		temp = temp.replace("\n","")
		if(len(temp) > 1):
			print "write", temp
			f.write(temp)
			if(multi_line == 1):
				f.write("\n")
	else:
		return
# Script starts from here
if len(sys.argv) < 2:
	print 'No action specified.'
	sys.exit()

if sys.argv[1].startswith('--'):
	option = sys.argv[1][2:]
# fetch sys.argv[1] but without the first two characters
	if option == 'version':
		print 'Version 1.1'
	elif option == 'help':
		print '''\
Options include:
  --version : Prints the version number
  --help    : Display this help'''
	else:
		print 'Unknown option.'
	sys.exit()
else:
	p1 = xml.parsers.expat.ParserCreate()
	p1.StartElementHandler = store_ori_start_element
	p1.EndElementHandler = store_ori_end_element
	try:
		rFile = open("ori_file",'r')
		p1.ParseFile(rFile)
	finally:
		rFile.close()
	print 'current ori array is:',ori_array
	print 'current ori_end array is:',ori_end_array
	len_ori = len(ori_array) 
	p2 = xml.parsers.expat.ParserCreate()
	p2.StartElementHandler = store_target_start_element
	p2.EndElementHandler =  store_target_end_element
	try:
		tFile = open("target_file",'r')
		p2.ParseFile(tFile)
	finally:
		tFile.close()
	print 'current target array is:',target_array
	print 'current target_end array is:',target_end_array
	len_target = len(target_array) 
	#p3 = xml.parsers.expat.ParserCreate()
	#seq = 0
	#p3.StartElementHandler = start_element
	#p3.EndElementHandler = end_element
	#p3.CharacterDataHandler = char_data
	for filename in sys.argv[1:]:
		p3 = xml.parsers.expat.ParserCreate()
		seq = 0
		cnt = 0
		p3.StartElementHandler = start_element
		p3.EndElementHandler = end_element
		p3.CharacterDataHandler = char_data
		fp = [ ]
		fp = os.path.split(filename) 
		fname = "db_" + fp[1]
		f = file(fname, 'w')
		f.write("<sheet>")
		try:
			inFile = open(filename,'r')
			print 'inFile is :', filename
			p3.ParseFile(inFile)
		finally:
			inFile.close()
			f.write("</sheet>")
			f.close
		del p3
		init_data()
