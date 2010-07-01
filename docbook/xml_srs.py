#!/usr/bin/python

import sys

fin = sys.argv[1]
fon = sys.argv[2]

start = 0
count = 0

try:
	fi = open(fin, 'r')
	fo = open(fon, 'w')
#write head
	fo.write("<chapter name=\"SRS\">\n");
	for line in fi:
		pt = line.find("\t")
		if ( line.find("_") != -1 ):
			head = line.find("\t")
			hs = line[:head]
			if (start == 1):
				fo.write("]]></annotation>\n")
			fo.write("<annotation xml:id=\"" + hs + " \" role=\"" + str(count) + "\" ><![CDATA[\n")
			fo.write(line)
			start = 1
			count = count + 1
		elif (line.find("\t") == 0):
			if(start == 1):
				fo.write("]]></annotation>\n")
				start = 0
			fo.write("<para>")
			fo.write("<![CDATA[")
			fo.write(line.strip())
			fo.write("]]>")
			fo.write("</para>\n")
		else:
			if(start == 1):
				fo.write(line)
	if(start == 1):
		fo.write("]]></annotation>\n")
		start = 0
	fo.write("</chapter>")
	count = 0
finally:
	fi.close()
	fo.close()
