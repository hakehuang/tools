#!/usr/bin/python
# parse_msxml.py <mxXSLexported.xml>
#
import xml.parsers.expat
import sys
import os
import re

class simplifyXML:
	def __init__(self):
		self.keep = 0
		self.ofd = 0
		self.p1 = re.compile("ss:")
		self.keeplist = ['Table','Row','Cell','Data']
	def start_element(self,name,attrs):
		if name in self.keeplist:
			self.keep = 1
		else:
			self.keep = 0
		if (self.keep ==  1):
			rename = self.p1.sub('',name)
			self.ofd.write("<"+rename.encode('ascii')+">");
		else:
			pass
	def end_element(self,name):
		if name in self.keeplist:
			self.keep = 1
		else:
			self.keep = 0
		if (self.keep == 1):
			rename = self.p1.sub("",name)
			self.ofd.write("</"+rename.encode('ascii')+">");
		else:
			pass
	def char_data(self,data):
		if (self.keep == 1):
			self.ofd.write(data.encode('utf-8'));
		else:
			pass
	def run(self,fn):
		try:
			self.parser = xml.parsers.expat.ParserCreate()
			self.parser.StartElementHandler = self.start_element
			self.parser.EndElementHandler = self.end_element
			self.parser.CharacterDataHandler = self.char_data
		except:
			print "xml parser create error"
			sys.exit()
		fd = open(fn,'r')
		inlist = os.path.split(fn);
		tp = "/s" + inlist[-1]
		outlist = list(inlist)
		outlist.pop()
		outlist.append(tp)
		self.ofd = open(''.join(outlist),'w')
		self.ofd.write("<?xml-stylesheet type=\"text/xsl\" href=\"srs_map_ce.xsl\"?>")
		self.parser.ParseFile(fd)
		del self.parser
		self.ofd.close()
		fd.close()


#main

fname = sys.argv[1]
mysim = simplifyXML()
mysim.run(fname)
del mysim

