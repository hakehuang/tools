#!/usr/bin/python
# case2srs.xml <srsfile.xml> <cases xml dir> <srscase map>
import xml.parsers.expat
import sys
import os
import re
#from sets import Set
import copy

from xml.dom.ext.reader import Sax2
from xml.dom import EMPTY_NAMESPACE

class searXMLonce:
	def __init__(self):
		self.reader = Sax2.Reader()
		self.data = ""
		self.sid = ""
	def searchByTag(self,fd,tag,sid):
		doc = self.reader.fromStream(fd)
		all_candidates = doc.getElementsByTagName(tag)
		self.data = ""
		for n in all_candidates:
			if n.firstChild.data == tag:
				tid = self.doc.getAttributeNS(EMPTY_NAMESPACE,'id')
				if (tid == sid):
					self.data = n.firstChild.data
					break
		del doc
		return
	def runfilesearch(self,fd,tag,sid):
		'''sid id to search, lists return the search result'''
		self.sid = sid
		self.searchByTag(tag,fd,tag,sid)
	def rundirsearch(self,dirs,tag,sid,relist):
		'''dirs directorys to search, sid searc id, lists return result'''
		if (os.path.isdir(dirs)):
			for i in os.listdir(dirs):
				if (os.path.isfile(dirs+i)):
					if(i.find(".xml") != -1):
						fd = open(dirs+i,'r')
						self.runfilesearch(fd,tag,sid)
						if (len(self.data):
							relist += self.data
		else:
			pass			

class serachXML:
	def __init__(self):
		self.dict = {}
		self.phase = 0
		self.stack = []
		self.searchindex = ""
		self.tag = ""
	def start_element(self,name,attrs):
		if (attrs.has_key(self.tag)):
			#print "search tag",name,self.tag,self.sid,attrs[self.tag]
			if(attrs[self.tag].encode('ascii') == self.sid):
				#start search
				self.phase = 1
			else:
				pass
		else:
			pass
		if (self.phase == 1):
			self.stack.append(name.upper().encode('ascii'))
			tlist = self.dict.keys()
			p = re.compile(r'/')
			#search possible match tag
			for i in tlist:
				#print "the list is ", i
				ttlist = p.split(i)
				if (ttlist == self.stack):
					#we get the same stack list
					self.searchindex = i
					break
				else:
					pass
				del ttlist
			del p
			del tlist
		else:
			pass
	def end_element(self,name):
		if (self.phase == 1):
			self.stack.pop()
			if (len(self.stack) == 0):
				self.phase = 0
			else:
				pass
			self.searchindex = ""
		else:
			pass
	def char_data(self,data):
		if (len(self.searchindex)):
			self.dict[self.searchindex] += data
			pass
		else:
			pass
	def AttlistDeclHandler(self,elname, attname, type, default, required):
		#print elname, attname, type, default, required
		pass
	def runfilesearch(self,fd,tag,sid,lists):
		try:
			self.parser = xml.parsers.expat.ParserCreate()
			self.parser.StartElementHandler = self.start_element
			self.parser.EndElementHandler = self.end_element
			self.parser.CharacterDataHandler = self.char_data
			self.parser.AttlistDeclHandler = self.AttlistDeclHandler
		except:
			print "xml parser create error"
			sys.exit()
		'''sid id to search, lists return the search result'''
		self.sid = sid
		self.dict.clear()
		self.dict = copy.deepcopy(lists)
		self.tag = tag
		self.parser.ParseFile(fd)
		del self.parser
	def rundirsearch(self,dirs,tag,sid,lists, relist):
		'''dirs directorys to search, sid searc id, lists return result'''
		self.sid = sid
		if (os.path.isdir(dirs)):
			for i in os.listdir(dirs):
				if (os.path.isfile(dirs+i)):
					if(i.find(".xml") != -1):
						fd = open(dirs+i,'r')
						self.runfilesearch(fd,tag,sid,lists)
						if (len(self.dict.values()) and len(self.dict.values()[0]) > 1 ):
							relist += self.dict.values()
		else:
			pass
			

class srscase:
	'''srs2case xml parser'''
	def __init__(self,fsrs,dcase):
		try:
			self.srsfd = open(fsrs,'r')
		except:
			print 'cannot open',fsrs
			sys.exit()
		self.casedir = dcase
		self.relist = []
		if (os.path.exists(dcase) == False ):
			self.casedir = null
			print 'dir ',dcase, 'does not exist'
			sys.exit()
		else:
			pass
		self.searchengine = serachXML()
	def getCaseListByID(self,sID, lists):
		'''get case detail inform'''
		del self.relist[:]
		self.searchengine.rundirsearch(self.casedir,"id",sID,lists,self.relist)
		self.searchengine.dict.clear()
	def getSRSListByIDOnly(self,srsID,lists):
		'''get all mapping srs detail inform'''
		del self.relist[:]
		mysearch = searXMLonce()
		mysearch.searchByTag(self.srsfd,"name",srsID)
		if ( len(mysearch.data) and len(mysearch.data) > 1):
			self.relist = mysearch.data
		del mysearch
	def getSRSListByID(self,srsID,lists):
		'''get all mapping srs detail inform'''
		del self.relist[:]
		#print "srsID",srsID
		#print "lists",lists
		self.searchengine.runfilesearch(self.srsfd,"name",srsID,lists)
		if ( len(self.searchengine.dict.values()) and len(self.searchengine.dict.values()[0]) > 1):
			self.relist = self.searchengine.dict.values()
		self.searchengine.dict.clear()
	
class outputXML:
	'''write to XML file'''
	def __init__(self,foutname):
		try:
			self.outfb = open(foutname,'w')
		except:
			print 'cannot open ',foutname
			sys.exit()
		self.writeXMLHead()
	def writeXMLHead(self):
		self.outfb.write("<?xml-stylesheet type=\"text/xsl\" href=\"srs_case.xsl\"?>\n")
		self.outfb.write("<chapter>\n")
		self.outfb.write("<title>srs to case mapping</title>\n")
	def writeXMLTail(self):
		self.outfb.write("\n</chapter>")
		self.outfb.close()
	def writeXMLContent(self,content,tag):
		self.outfb.write("<")
		self.outfb.write(tag)
		self.outfb.write(">\n")
		self.outfb.write("<![CDATA[")
		self.outfb.write(content.encode('utf-8'))
		self.outfb.write("]]>")
		self.outfb.write("\n")
		self.outfb.write("</")
		self.outfb.write(tag)
		self.outfb.write(">\n")
	def writeXMLStart(self,content,tag):
		self.outfb.write("<")
		self.outfb.write(tag)
		self.outfb.write(">\n")
		self.outfb.write("<![CDATA[")
		self.outfb.write(content.encode('utf-8'))
		self.outfb.write("]]>")
	def writeXMLEnd(self,tag):
		self.outfb.write("</")
		self.outfb.write(tag)
		self.outfb.write(">\n")

#main
p1 = re.compile(r'\s')
p2 = re.compile(r',')
#generate case2srs
flsrs = sys.argv[1]
drcase = sys.argv[2]
srscasemap = sys.argv[3]
mymap = open(srscasemap,'r')
#1 get all cases ID from srscasemap file
cases = []
for i in mymap:	
	if (len(i) == 0 or i[0] == "#"):
		continue
	ii = p1.split(i)
	if ( len(ii) == 0):
		continue
	results = p2.split(ii[1])
	cases += results
allcases = set(cases)
print len(allcases)
#search srs mapped to case
myoutput = outputXML("case2srs_map.xml")
for i in allcases:
	if (len(i) == 0 or i[0] == "#"):
		continue
	ii = p1.split(i)
	if ( len(ii) == 0):
		continue
	myoutput.writeXMLStart("","sect1")
	print "i =", i
	myoutput.writeXMLContent(i,"title")
	p3 = re.compile(i)
	mymap.seek(0)
	for j in mymap:
		if (len(j) == 0 or j[0] == "#"):
			continue
		lj = p1.split(j)
		if ( len(lj) == 0):
			continue
		jj = p3.search(str(j))
		mysrscase = srscase(flsrs,drcase)
		if (len(str(jj))):
			ii = p1.split(j)
			lists = {}
			lists['formalpara/para'.upper()] = ""
			mysrscase.getSRSListByID(ii[0],lists)
			if (len(mysrscase.relist)):
				myoutput.writeXMLStart("","formalpara")
				myoutput.writeXMLContent(mysrscase.relist[0],"para")
				myoutput.writeXMLEnd("formalpara")
		del mysrscase
	myoutput.writeXMLEnd("sect1")

myoutput.writeXMLTail()
mymap.close()
