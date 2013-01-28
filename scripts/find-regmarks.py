#!/usr/bin/python
import sys
import re
import json
from os import listdir
from os.path import isfile, join

htmldir=sys.argv[1]
reg=u"\u00AE"
regf=re.compile('\>([\w\s]+)\w'+reg,re.UNICODE)
reglist={}
onlyfiles = [ f for f in listdir(htmldir) if isfile(join(htmldir,f)) ]
for fd in onlyfiles:
	data=""
	with open (htmldir+'/'+fd, "r") as myfile:
		data=myfile.read()
		for a in regf.findall(data):
			if len(a)>2:
				reglist[a.strip()]=1

print json.dumps(sorted(reglist.keys()),indent=4)
