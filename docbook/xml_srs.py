#!/usr/bin/python
#generate the srs reprot sheet
#command line:
#xml_srs.py <the SRS blank file> <xml file you want output>
#e.g.
#./xml_srs.py ../mx50_test_manual/SRS/mx508_SRS_release SRS_release.xml

import sys

fin = sys.argv[1]
fon = sys.argv[2]

start = 0
count = 0
hsect = 0
try:
	fi = open(fin, 'r')
	fo = open(fon, 'w')
#write head
	fo.write("<?xml-stylesheet type=\"text/xsl\" href=\"srs_list.xsl\"?>\n");
	fo.write("<chapter name=\"SRS\"><title>SRS List</title>\n");
	for line in fi:
		pt = line.find("\t")
		if ( line.find("_") != -1 ):
			head = line.find("\t")
			hs = line[:head]
			if (start == 1):
				fo.write("]]></para></formalpara>\n")
			fo.write("<formalpara name=\"" + hs + "\" count=\"" + str(count) + "\" >")
			fo.write("\n<title>" + hs + "</title>\n")
			fo.write("<para><![CDATA[\n")
			fo.write(line)
			start = 1
			count = count + 1
		elif (line.find("\t") == 0):
			if(start == 1):
				fo.write("]]></para></formalpara>\n")
				start = 0
			if (hsect == 1):
				fo.write("</sect1>\n")
				hsect = 0
			if (line.strip() != ''):
				fo.write("<sect1>")
				fo.write("<title><![CDATA[")
				fo.write(line.strip())
				fo.write("]]></title>")
				hsect = 1
		else:
			if(start == 1):
				fo.write(line)
	if(start == 1):
		fo.write("]]></para></formalpara>\n")
		start = 0
	if (hsect == 1):
		fo.write("</sect1>\n")
		hsect = 0
	fo.write("</chapter>")
	count = 0
finally:
	fi.close()
	fo.close()
