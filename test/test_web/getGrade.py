#! /usr/bin/python
# -*- coding: utf8 -*-

import urllib,json
import urllib2


def getResult():
	op="create"
	url = 'http://127.0.0.1:8000/'+op
	#url = 'http://172.29.152.242:8000/'+op
	path="/home/hitnslab/docker/demo/data/"+op+".json"
	with open(path, "r") as f:
		data= json.load(f)
	op_list=op.split("_")
	values={}
	if len(op_list)==2:
		keys=op_list[0]+op_list[1]+"json"
	else:
		keys=op_list[0]+"json"
	values[keys]=json.dumps(data)
	
	data = urllib.urlencode(values)
	req = urllib2.Request(url,data)
	response = urllib2.urlopen(req)
	sourceCode = response.read()
	print dict(eval(sourceCode))


if __name__ == '__main__':
	getResult()
	
