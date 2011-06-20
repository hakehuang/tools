#!/usr/bin/python
# srs_case_map.py srs.xml <case.xml dir> srs_case_map
#
import xml.parsers.expat
import sys
import os
import re

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
		self.dict = lists
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
	def getSRSListByID(self,srsID,lists):
		'''get all mapping srs detail inform'''
		del self.relist[:]
		self.searchengine.runfilesearch(self.srsfd,"name",srsID,lists)
		if ( len(self.searchengine.dict.values())):
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
		self.outfb.write(content.encode("utf-8"))
		self.outfb.write("\n")
		self.outfb.write("</")
		self.outfb.write(tag)
		self.outfb.write(">\n")
	def writeXMLStart(self,content,tag):
		self.outfb.write("<")
		self.outfb.write(tag)
		self.outfb.write(">\n")
		self.outfb.write(content.encode("utf-8"))
	def writeXMLEnd(self,tag):
		self.outfb.write("</")
		self.outfb.write(tag)
		self.outfb.write(">\n")

class outputText:
	'''write to plain text'''
	def __init__(self,foutname):
		try:
			self.outfb = open(fountname,'w')
		except:
			print 'cannot open ', foutname
			sys.exit()
	def writecontent(self, content):
		self.outfb.write(content)
		self.outfb.write("\n")
	def closefile(self):
		self.outfb.close()


#main
flsrs = sys.argv[1]
drcase = sys.argv[2]
srscasemap = sys.argv[3]

#generate srs2case
myoutput = outputXML("srs2case_map.xml")
myoutput.writeXMLHead()
mymap = open(srscasemap,'r')
p1 = re.compile(r'\s')
p2 = re.compile(r',')
p3 = re.compile(r'-')
for i in mymap:
	skip = 0
	if (len(i) == 0 or i[0] == "#"):
		continue
	ii = p1.split(i)
	if (len(ii) == 0):
		continue
	mysrscase = srscase(flsrs,drcase)
	lists = {}
	lists['formalpara/para'.upper()] = ""
	#print ii[0]
	mysrscase.getSRSListByID(ii[0],lists)
	if (len(mysrscase.relist)):
		myoutput.writeXMLStart("","sect1")
		#print "SRS list by srsID",mysrscase.relist
		myoutput.writeXMLContent(mysrscase.relist[0],"title")
	else:
		skip = 1
	del mysrscase
	lists.clear()
	if (skip == 1):
		continue
	k = ''.join(ii[1:])
	del ii
	results = p2.split(k)
	for j in results:
		myoutput.writeXMLStart("","formalpara")
		if p3.search(j):
			myoutput.writeXMLStart(j,"title name="+"\""+j+"\"")
		else:
			myoutput.writeXMLStart(j,"title")
		myoutput.writeXMLEnd("title")
		lists['sect1/title'.upper()] = ""
		mysrscase =  srscase(flsrs,drcase)
		mysrscase.getCaseListByID(j,lists)
		if (len(mysrscase.relist)):
			print "case list by srsID",mysrscase.relist
			myoutput.writeXMLContent(mysrscase.relist[0],"para")
		del mysrscase
		lists.clear()
		myoutput.writeXMLEnd("formalpara")
	myoutput.writeXMLEnd("sect1")
myoutput.writeXMLTail()
del myoutput

mymap.close()
