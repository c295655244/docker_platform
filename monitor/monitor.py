#! /usr/bin/env python
#-*-coding:utf-8-*-

import sys,os
import httplib,urllib
import json
import time
import datetime

class Docker(object):
	def __init__(self):
		super(Docker, self).__init__()
		self.conn=httplib.HTTPConnection('0.0.0.0:2375')

	#获取docker列表
	def GetDockerList(self):
		try:
			self.conn.request("GET", "/containers/json?all=1")
			r1 = self.conn.getresponse()
		except Exception,e:
				print Exception
		raw = r1.read()
		data=json.loads(raw)
		list_data=[]
		#print data
		for item in data:
			dict_data={}
			ltime=time.localtime(item["Created"])
			dict_data["created_time"]=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
			dict_data["docker_id"]=item["Names"][0].replace("/","")
			dict_data["image"]=item["Image"]
			dict_data["command"]=item["Command"]
			dict_data["status"]=item["Status"]
			list_data.append(dict_data)
		print list_data


	#获取单个docker信息
	def GetDockerInfo(self,docker_id):
		try:
			self.conn.request("GET", "/containers/%s/stats?stream=0"%(docker_id))
			r2=self.conn.getresponse()
		except Exception,e:
			print Exception
		dic=r2.read()
		d=json.loads(dic)
		print d
		time=d["read"]
		self.systemtime=time.split('.')[0]
		print "containerID",docker_id
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


	def main(self):
		pass
	
if __name__ == '__main__':
	demo=Docker()
	#demo.GetDockerList()
	demo.GetDockerInfo("test_ubuntu_1")



