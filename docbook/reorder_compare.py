#!/usr/bin/python
# diff two exec table according to case ID
# ./reorder_compare.py -i new_exec_table -I old_exec_table -o outputfile
# e.g.
# ./reorder_compare.py -i exec_table -I exec_table2 -o diff_exec_table

import os
import sys
import time
import getopt

df = "exec_table"
xf = "exec_table2"
of = "diff_exec_table"

def usage():
	print "-h: this help"
	print "-I <xiaotian export cmd line file>"
	print "-i <p_parser.py output cmd file>"
	print "-o output cmdfile differ"

try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:I:o:",\
	["help", "Pattern=","Attrib=","Output="])
except getopt.error, msg:
	print msg
	print "for help use --help"
	sys.exit(2)
for o,a in opts:
	if o in ("-h", "--help"):
		usage()
		exit(0)
	if o in ("-i", "--in"):
		df = a
	if o in ("-I","--Input"):
		xf = a
	if o in ("-o","--Output"):
		of = a

#print "process :", args

pdf = file(df,'r')
pxf = file(xf,'r')
pof = file(of,'w')

for line in pdf:
	case = line.split('\t')
	title = case[0]
	cmd1 = case[1].rstrip().strip()
	pxf.seek(0)
	for line2 in pxf:
		case2 = line2
		lx = line2.find(" ")
		title2 = line2[:lx]
		cmd2 = line2[lx+1:].rstrip().strip()
		if (title2 == title):
			if(cmd1 != cmd2):
				print 'case diff:', title
				print 'should be:', cmd1
				print 'but is:', cmd2
				pof.write("\n++++++++++++\n")
				pof.write(str(title)+"\n")
				pof.write(str(cmd1)+"\n")
				pof.write("\n----------\n")
				pof.write(str(cmd2))

