#! /usr/bin/env python
#-*-coding:utf-8-*-

import sys,os
import httplib,urllib
import json
import time
import datetime
import traceback

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
			self.conn.request("GET", "/containers/%s/stats?stream=1"%(docker_id))
			while 1:
				r2=self.conn.getresponse()
				dict_data=r2.read()
				data=json.loads(dict_data)
				print 1
		except Exception,e:
			print "不存在id为：",docker_id,"的容器！"
			print traceback.format_exc()
			return 
		print data
		# print "containerID",docker_id






	#获取流量信息
	def GetFlow(data):
		network={}
		if 'networks' in data:
			networks_data=data['networks']
			for interface in networks_data.keys():
				network[interface]={}
	 			content=networks_data[interface]
	 			network[interface]["rx"]=content['rx_bytes']
	 			network[interface]["tx"]=content['tx_bytes']

	 	print network
	 	return network

	#获取cpu信息
	def GetCpu(data):
		cpu_stats=data['cpu_stats']
	 	cpu_usage=cpu_stats['cpu_usage']
	 	self.cpu_usage_in_usermode=cpu_usage['usage_in_usermode']
	 	self.cpu_total_usage=cpu_usage['total_usage']
	 	self.cpu_system_cpu_usage=cpu_stats['system_cpu_usage']
	 	print 'cpu_usage_in_usermode: ',self.cpu_usage_in_usermode
	 	print 'cpu_total_usage: ',self.cpu_total_usage
	 	print 'cpu_system_cpu_usage: ',self.cpu_system_cpu_usage

	 			

	#获取内存信息
	def GetMem(data):
	 	memory_stats=data['memory_stats']
	 	mem_usage=memory_stats['usage']
	 	mem_limit=memory_stats['limit']
	 	if mem_limit!=0:
	 		self.mem_percentage = round(float((float(mem_usage)/float(mem_limit))*100), 3)
	 	else:
	 		self.mem_percentage = 0
	 	print "mem usage :",str(self.mem_percentage)+'%'
	 	print "==================================================="
	


if __name__ == '__main__':
	demo=Docker()
	#demo.GetDockerList()
	demo.GetDockerInfo("grave_bhabha")



