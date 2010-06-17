#!/usr/bin/python

import xml.parsers.expat
import sys

#virables
ori_array = [ ]
target_array = [ ]
seq = 0
add_content = 0

# 3 store the  
def store_ori_start_element(name, attrs):
	ori_array.append(name);
def store_target_start_element(name, attrs):
	target_array.append(name);
# 3 handler functions
def start_element(name, attrs):
	global add_content
	global seq
	global len_ori
	global ori_array
	global target_array
	global f
	add_content = 0
	print 'Start element:', name, attrs
	if( seq < len_ori and len(ori_array) > 1):
		if (name == ori_array[seq] or "skip" == ori_array[seq]):
			if( name == ori_array[seq]):
				f.write("\n<")
				f.write(target_array[seq]);
				f.write(">")
				add_content = 1
			seq = seq + 1
	else:
		seq = 0	
def end_element(name):
	global add_content
	global seq
	global len_ori
	global ori_array
	global target_array
	global f
	print 'End element:', name
	if (add_content == 1 and len(target_array) > 1 ):
		f.write("\n<")
		f.write(target_array[seq - 1])
		f.write(">")
def char_data(data):
	global add_content
	global seq
	global len_ori
	global ori_array
	global target_array
	global f
	if(data == '\n'):  
		return  
	if(data.isspace()):  
		return  
	print 'Character data:', repr(data)
	temp = repr(data)
	tl = len(temp)
	if(add_content == 1):
		f.write("\n")
		f.write(repr(data)[2:tl-1].replace("\\t",""))
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
	try:
		rFile = open("ori_file",'r')
		p1.ParseFile(rFile)
	finally:
		rFile.close()
	print 'current ori array is:',ori_array
	len_ori = len(ori_array) 
	p2 = xml.parsers.expat.ParserCreate()
	p2.StartElementHandler = store_target_start_element
	try:
		tFile = open("target_file",'r')
		p2.ParseFile(tFile)
	finally:
		tFile.close()
	print 'current target array is:',target_array
	len_target = len(target_array) 
	f = file('db.xml', 'w')
	p3 = xml.parsers.expat.ParserCreate()
	seq = 0
	p3.StartElementHandler = start_element
	p3.EndElementHandler = end_element
	p3.CharacterDataHandler = char_data
	for filename in sys.argv[1:]:
		try:
			inFile = open(filename,'r')
			p3.ParseFile(inFile)
		finally:
			inFile.close()

