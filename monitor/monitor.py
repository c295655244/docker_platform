#! /usr/bin/env python
#-*-coding:utf-8-*-

import sys,os
import httplib,urllib
import json
from collections import OrderedDict
import pprint

import time

class Docker(object):
	def __init__(self):
		super(Docker, self).__init__()
	def GetDockerList(self):
		try:
			conn=httplib.HTTPConnection('0.0.0.0:2375')
			conn.request("GET", "/containers/json?all=1")
			r1 = conn.getresponse()
		except Exception,e:
				print Exception
		raw = r1.read()
		data=json.loads(raw)
		docker_list=[item["Names"][0].replace("/","") for item in data]
		print docker_list

	def GetDockerInfo(self,docker_list):
		





	def main(self):
		pass
	
if __name__ == '__main__':
	demo=Docker()
	demo.GetDockerList()


