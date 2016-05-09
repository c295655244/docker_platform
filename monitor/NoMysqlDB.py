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
	def obtainDockerStates(self):
		try:
			print "start"
			conn=httplib.HTTPConnection('0.0.0.0:2375')
			conn.request("GET", "/containers/json?all=1")
			r1 = conn.getresponse()
		except Exception,e:
				print Exception
		raw = r1.read()
		data=json.loads(raw)

		for key in data:
			containerID=key['Id']#DockerID
			containerName=key['Names'][0]#DockerName
			containerImage=key['Image']#Which Image
			print containerName
			try:
				conn=httplib.HTTPConnection('0.0.0.0:2375')
				conn.request("GET", "/containers/%s/stats?stream=0"%(containerID))
				r2=conn.getresponse()
			except Exception,e:
				print Exception
			dic=r2.read()
			d=json.loads(dic)
			#print d
			time=d["read"]
			self.systemtime=time.split('.')[0]
			if self.systemtime != "0001-01-01T00:00:00Z":
				print 'systemtime: ',self.systemtime
				print "containerID",containerID
				print "containerName",containerName
				print "containerImage",containerImage


			 	if 'networks' in d:
			 		if 'eth0' in d['networks']:
			 			networks=d['networks']
			 			content=networks['eth0']
			 			self.rx_bytes=content['rx_bytes']
			 			self.tx_bytes=content['tx_bytes']
			 			print "RX:",self.rx_bytes
			 			print "TX:",self.tx_bytes

			 	cpu_stats=d['cpu_stats']
			 	cpu_usage=cpu_stats['cpu_usage']
			 	self.cpu_usage_in_usermode=cpu_usage['usage_in_usermode']
			 	self.cpu_total_usage=cpu_usage['total_usage']
			 	self.cpu_system_cpu_usage=cpu_stats['system_cpu_usage']

			 	print 'cpu_usage_in_usermode: ',self.cpu_usage_in_usermode
			 	print 'cpu_total_usage: ',self.cpu_total_usage
			 	print 'cpu_system_cpu_usage: ',self.cpu_system_cpu_usage

			 	memory_stats=d['memory_stats']
			 	mem_usage=memory_stats['usage']
			 	mem_limit=memory_stats['limit']
			 	if mem_limit!=0:
			 		self.mem_percentage = round(float((float(mem_usage)/float(mem_limit))*100), 3)

			 	else:
			 		self.mem_percentage = 0
			 	print "mem usage :",str(self.mem_percentage)+'%'

			 	print "==================================================="

			else:
			 	continue
if __name__ == '__main__':
	d=Docker()
	d.obtainDockerStates()


