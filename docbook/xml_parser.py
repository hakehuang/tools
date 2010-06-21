#!/usr/bin/python

import xml.parsers.expat
import sys
import os

#virables
ori_array = [ ]
ori_end_array = [ ]
target_array = [ ]
target_end_array = [ ]
sa = [ ]
seq = 0
seq_end = 0
add_content = 0
# 3 store the  
def store_ori_start_element(name, attrs):
	ori_array.append(name);
def store_ori_end_element(name):
	ori_end_array.append(name);
def store_target_start_element(name, attrs):
	target_array.append(name);
def store_target_end_element(name):
	target_end_array.append(name);
# 3 handler functions
def start_element(name, attrs):
	global add_content
	global seq
	global len_ori
	global ori_array
	global target_array
	global f
	global sa
	print 'Start element:', name, attrs, seq, len_ori
	if (seq < len_ori and name == ori_array[seq]):
		if( "skip" == target_array[seq]):
			add_content = 0
		elif ("char" == target_array[seq]):
			add_content = 1
		else:
			f.write("\n<")
			f.write(target_array[seq]);
			f.write(">")
			add_content = 1
		if(seq < len_ori):
			seq = seq + 1
	else:
		#abnormal happen
		add_content = 0
		if(seq > 0 and seq < len_ori - 1):
			print 'abnormal!!!', name, ori_array[seq],seq
			#try to use the parent attribute
			if(len(sa)):
				add_content = sa[-1]
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
	print 'End element:', name
	if (seq_end >= len(ori_end_array)):
		seq_end = 0
		seq = 0
	if (name == ori_end_array[seq_end] and seq > 0):
		if(target_end_array[seq_end] == "char" ):
			pass
		elif("skip" == target_end_array[seq_end]):
			pass
		else:
			f.write("\n</")
			f.write(target_end_array[seq_end])
			f.write(">")
		seq_end = seq_end + 1
	else:
		pass
		#abnormal happen
		#print 'end abnormal!!!', name , ori_end_array[seq_end], seq_end
	sa.pop()
	return
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
	p3 = xml.parsers.expat.ParserCreate()
	seq = 0
	p3.StartElementHandler = start_element
	p3.EndElementHandler = end_element
	p3.CharacterDataHandler = char_data
	for filename in sys.argv[1:]:
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

