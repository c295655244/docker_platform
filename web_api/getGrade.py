#! /usr/bin/python
# -*- coding: utf8 -*-

import urllib,json
import urllib2



def getResult():
	#url = 'http://127.0.0.1:8000/create'
	url = 'http://172.29.152.242:8000/create'
	path="/home/docker/docker/demo/data/create.json"
	with open(path, "r") as f:
		data= json.load(f)
	
	values = {
		'createjson':json.dumps(data)
	}
	data = urllib.urlencode(values)
	req = urllib2.Request(url,data)
	response = urllib2.urlopen(req)
	sourceCode = response.read()
	print dict(eval(sourceCode))


if __name__ == '__main__':
	getResult()
	
