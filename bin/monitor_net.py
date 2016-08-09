#! /usr/bin/env python
#-*-coding:utf-8-*-
import sys,re
import json
import time
import datetime
import traceback
import httplib,urllib
import subprocess 
import libvirt 
from xml.etree import ElementTree as ET 
from read_data import *
from db_operate import *



class MonitorNet():

	def __init__(self):
		self.config=ReadDockConf()
		self.mongo=MongoOperate(self.config)
		self.db=MysqlOperate(self.config)


	def DockerNetMonitor(self):
		current_dict={}
		pattern = re.compile(r'RX bytes:(.*?) \(.* MB\)  TX bytes:(.*?) \(.* KB\)')
		while 1:
			docker_list=self.mongo.display_tpl("monitor_flag")[0]["docker_list"]
			if docker_list[0] not in current_dict.keys():
				current_dict={}
			for item in docker_list:
				cmd="sudo docker exec %s ifconfig"%item
				proc = subprocess.Popen(cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
				out=proc.stdout.read()
				if "Error" in out:
					continue
				match = pattern.findall(out)
				input_kb=0
				output_kb=0
				for net_bytes in match:
					input_kb+=float(net_bytes[0])/1000
					output_kb+=float(net_bytes[1])/1000
				if item not in current_dict.keys():
					current_dict[item]={
						"time":datetime.datetime.now(),
						"input_kb":input_kb,
						"output_kb":output_kb,
						"input_rate":0.0,
						"output_rate":0.0
					}
				else:
					current_t=datetime.datetime.now()
					diff=current_t-current_dict[item]["time"]
					t_diff=float(str(diff)[-8:])
					input_rate=(input_kb-current_dict[item]["input_kb"])/t_diff
					output_rate=(output_kb-current_dict[item]["output_kb"])/t_diff
					current_dict[item]["input_rate"]=float('%0.2f'%input_rate)
					current_dict[item]["output_rate"]=float('%0.2f'%output_rate)
					current_dict[item]["input_kb"]=input_kb
					current_dict[item]["output_kb"]=output_kb					
					current_dict[item]["time"]=current_t
			print "docker网络流量更新成功！",docker_list
			time.sleep(0.7)
			self.db.save_docker_net_stats(current_dict)


if __name__ == '__main__':
	demo=MonitorNet()
	demo.DockerNetMonitor()
