#!/usr/bin/python
# get all case from srs_case_map
# getallcase.py <srscasemap>
import sys
import os
import re

mymap = open(sys.argv[1],'r')
p1= re.compile(r'\s')
p2= re.compile(r',')
p3 = re.compile(r'-')
list = []
for i in mymap:
		ii = p1.split(i)
		j = p2.split(ii[1])
		for jj in j:
			if p3.search(jj):
				list.append(jj)
			else:
				pass

outlist = set(list)
del list

for i in outlist:
	print i
