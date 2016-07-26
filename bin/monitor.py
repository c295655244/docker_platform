#! /usr/bin/env python
#-*-coding:utf-8-*-
import sys
import json
import time
import traceback
import httplib,urllib
import subprocess 
import datetime
from read_data import *
from db_operate import *



class Monitor(object):

	def __init__(self):
		super(Monitor, self).__init__()
		#连接本地docker demon
		self.conn=httplib.HTTPConnection('0.0.0.0:2375')
		self.config=ReadDockConf()
		self.db=MysqlOperate(self.config)

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
			dict_data["id"]=item["Id"][0:12]
			dict_data["name"]=item["Names"][0].replace("/","")
			dict_data["image"]=item["Image"]
			dict_data["command"]=item["Command"]
			if "Up" in item["Status"]:
				dict_data["status"]="run"
			elif "Exited" in item["Status"]:
				dict_data["status"]="stop"
			else:
				dict_data["status"]="fault"
			list_data.append(dict_data)
		#print list_data
		return  list_data


	#去除多余空格		
	def DelSerialSpace(self,str_data):
		while str_data.find("  ")!=-1:
			str_data=str_data.replace('  ',' ')
		return str_data

	#格式化数据
	def DockerStatsParse(self,data):
		data_dict={}	
		data_dict["id"]=data[0]
		data_dict["cpu"]=float(data[1].replace("%",""))
		data_dict["mem"]=float(data[7].replace("%",""))

		#流量数制转换(base on B)
		if data[9]=="B":
			data_dict["net_input"]=0.0
		elif data[9]=="MB":
			data_dict["net_input"]=float(data[8])*1024
		elif data[9]=="GB":
			data_dict["net_input"]=float(data[8])*1024*1024
		else:
			data_dict["net_input"]=float(data[8])

		if data[12]=="B":
			data_dict["net_output"]=0.0
		elif data[12]=="MB":
			data_dict["net_output"]=float(data[11])*1024
		elif data[12]=="GB":
			data_dict["net_output"]=float(data[11])*1024*1024
		else:
			data_dict["net_output"]=float(data[11])

		data_dict["input_rate"]=0.0
		data_dict["output_rate"]=0.0
		return data_dict


	#计算流量速度
	def CalFlowRate(self,old_data,now_data,t_diff):
		for docker_id in now_data.keys():
			#若是新加入的docker
			if docker_id not in old_data.keys():
				now_data[docker_id]["input_rate"]=0.0
				now_data[docker_id]["output_rate"]=0.0
			else:
				input_rate=(now_data[docker_id]["net_input"]-old_data[docker_id]["net_input"])/t_diff
				output_rate=(now_data[docker_id]["net_output"]-old_data[docker_id]["net_output"])/t_diff
				now_data[docker_id]["input_rate"]=float('%0.2f'%input_rate)
				now_data[docker_id]["output_rate"]=float('%0.2f'%output_rate)
				#print input_rate,output_rate
		return now_data



	def DockerMonitor(self):
		cmd = subprocess.Popen('sudo docker stats -a',stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
		stats_dict={}
		stats_dict_old={}	
		t_start=datetime.datetime.now()
		update_count=0#计数，状态更新10次，进行一次id与name的添加删除操作
		self.db.save_host_id_stats(self.GetDockerList())
		while 1:
			stats_output = cmd.stdout.readline()
			stats_output=self.DelSerialSpace(stats_output)
			stats=stats_output.split(" ")

			if "CPU" not in stats:
				#print stats
				stats_parse=self.DockerStatsParse(stats)
				stats_dict[stats_parse["id"]]=stats_parse

			elif stats_dict!={}:
				#计算时间差
				t_end=datetime.datetime.now()
				diff=t_end-t_start
				t_start=t_end
				t_diff=float(str(diff)[-8:])

				if stats_dict_old!={}:
					#计算网速
					stats_dict=self.CalFlowRate(stats_dict_old,stats_dict,t_diff)

				stats_dict_old=stats_dict

				#sql操作,更新当前host状态
				result_flag=self.db.save_host_stats(stats_dict)

				#没刷新10次，查询一下是否由新的host加入，是否有旧的host需要删除
				if update_count>10:
					#获取docker_list
					current_host_list=self.GetDockerList()

					#此处获取kvm_list
					pass

					self.db.save_host_id_stats(current_host_list)					
					self.db.del_host_id_stats(current_host_list)
					self.db.save_host_stats_flag(current_host_list)

					update_count=0

				update_count+=1
				print "状态数据更新！"
				#print stats_dict
				stats_dict={}



if __name__ == '__main__':
	demo=Monitor()
	#demo.GetDockerList()
	demo.DockerMonitor()
