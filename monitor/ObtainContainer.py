#! /usr/bin/env python
#-*-coding:utf-8-*-

import sys,os
import httplib,urllib
import json
from collections import OrderedDict
import pprint
import MySQLdb
from pymysql import PyMysql
import time
class Docker(object):
	def __init__(self):
		super(Docker, self).__init__()
		"""
		请改ClusterIP
		"""
		self.ClusterIP=['172.29.152.185','172.29.152.186','172.29.152.188',\
		'172.29.152.181','172.29.152.182','172.29.152.183','172.29.152.184',\
		'172.26.253.30','172.29.152.187','172.29.152.189']

		self.db = PyMysql('172.29.152.185','xzbMysql','000','moniter')

		self.swarmPort=2375
		self.mem_percentage=0
		self.systemtime=None
		self.cpu_usage_in_usermode=None
		self.cpu_total_usage=None
		self.cpu_system_cpu_usage=None
		self.rx_bytes=None
		self.tx_bytes=None

	def obtainDockerStates(self):
		mem_limit=0
		mem_usage=0
		for item in self.ClusterIP:#Slave'sIPAddress

			try:
				conn=httplib.HTTPConnection('%s:%d'%(item,self.swarmPort))
				conn.request("GET", "/containers/json?all=1")
				r1 = conn.getresponse()
				#print r1.status,r1.reason,r1.read()#str
			except Exception,e:
				print 'GET error \n'
			raw = r1.read()
			data=json.loads(raw)

			for key in data:
			 	containerID=key['Id']#DockerID
			 	containerName=key['Names'][0]#DockerName
			 	containerImage=key['Image']#Which Image

			 	try:
			 		conn=httplib.HTTPConnection('%s:%d'%(item,self.swarmPort))
			 		conn.request("GET", "/containers/%s/stats?stream=0"%(containerID))
			 		r2=conn.getresponse()
			 		#print r2.status,r2.reason
			 	except Exception,e:
			 		print Exception
			 	dic=r2.read()
			 	d=json.loads(dic)
			 	time=d["read"]
			 	self.systemtime=time.split('.')[0]
			 	#query time 

			 	if self.systemtime != "0001-01-01T00:00:00Z":
			 		print 'systemtime: ',self.systemtime
			 		sql="insert ignore into Container (HostIP,ContainerID) values('%s','%s')"%(item,containerID)
			 		self.db.update(sql)
			 		print "MYSQL INSERT SUCCESS"

			 		if 'networks' in d:#network
			 			if 'eth0' in d['networks']:
			 				networks=d['networks']
			 				content=networks['eth0']
			 				self.rx_bytes=content['rx_bytes']
			 				self.tx_bytes=content['tx_bytes']
			 				print "RX:",self.rx_bytes
			 				print "TX:",self.tx_bytes
			 				net_sql="update Container set rx_bytes=%s, tx_bytes=%s where ContainerID='%s'"%\
			 				(self.rx_bytes,self.tx_bytes,containerID)
			 				self.db.update(net_sql)
			 				print "MYSQL UPDATE SUCCESS"
			 		#Block IO
			 		#blkio_stats=d["blkio_stats"]
			 		#for io_kv in blkio_stats:
			 		#	pass#print io_kv,blkio_stats[io_kv]


			 		#CPU Moniter
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

			 		sql2="update Container set ContainerName='%s', Image='%s',time='%s', cpu_usage_in_usermode=%s, \
			 		cpu_total_usage=%s, cpu_system_cpu_usage=%s, \
			 		mem_percentage=%.2f where ContainerID='%s'"%\
			 		(str(containerName),\
			 			str(containerImage),\
			 			str(self.systemtime),\
			 			self.cpu_usage_in_usermode,\
			 			self.cpu_total_usage,\
			 			self.cpu_system_cpu_usage,\
			 			self.mem_percentage,\
			 			containerID)
			 		self.db.update(sql2)
			 		print "MYSQL UPDATE SUCCESS"
			 		print "==================================================="
			 	else:
			 		continue
			 		

if __name__ == '__main__':
	d=Docker()
	#3while(True):
	start = time.time()
	d.obtainDockerStates()
	end = time.time()
	print end-start
	#	time.sleep(10)
	

