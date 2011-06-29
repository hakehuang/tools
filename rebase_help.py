#!/usr/bin/python

import sys
import os
import re
import copy
import commands

p1 = re.compile(r'\n')

class rebase:
	def __init__(self, fname):
		self.slists = []
		self.elists = []
		self.fname = fname
		self.dicts = {}
		pass
	def replace_regions(self,start,end):
		ret = commands.getstatusoutput("grep -n " + start + " " + self.fname + "| grep -v \"========\"| cut -d : -f 1")
		if (ret[0] == 0):
			temp = ret[1:]
			self.slists = p1.split(temp[0])
		print 'start list',self.slists
		del ret
		ret = commands.getstatusoutput("grep -n " + end + " " + self.fname + "| cut -d : -f 1")
		if (ret[0] == 0):
			temp = ret[1:]
			self.elists =  p1.split(temp[0])
		del ret
		print 'end list',self.elists
		if (len(self.slists) != len(self.elists)):
			print "file match error"
			return
		self.dicts = dict(zip(self.slists,self.elists))
		print "dictions", self.dicts
		for i in self.dicts:
			command = "sed "  + "-i "  +"\'" + i + "," + self.dicts[i] + "s/^.*/QWERTYUI/\'" + " " + self.fname
			ret = commands.getstatusoutput(command)
		del self.dicts
		del self.slists
		del self.elists
		command = "sed -i " + "\'/" + "QWERTYUI" + "/d\'" + " " + self.fname
		print command
		ret = commands.getstatusoutput(command)
	def replace_heads(self,head):
		command = "sed -i " + "\'/" + head + "/d\'" + " " + self.fname
		print command
		ret = commands.getstatusoutput(command)

			


myrebase = rebase(sys.argv[1])

myrebase.replace_regions("=======","\>\>\>\>")
myrebase.replace_heads("<<<<<<")
