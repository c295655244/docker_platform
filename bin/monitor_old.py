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



class Monitor(object):

	def __init__(self):
		super(Monitor, self).__init__()
		#连接本地docker demon
		#需要提前更改/etc/default/docker文件，添加：DOCKER_OPTS="-H=unix:///var/run/docker.sock -H=0.0.0.0:6732" 
		self.conn=httplib.HTTPConnection('0.0.0.0:6732')
		self.config=ReadDockConf()
		self.db=MysqlOperate(self.config)

	#获取kvm列表
	def GetKvmList(self):
		conn = libvirt.open('qemu:///system') 
		dom = conn.listDomainsID()
		list_data=[]
		for i in dom: 
			dict_data={}
			vmm_id = conn.lookupByID(i) 
			vmm_name = vmm_id.name()
			dict_data["id"]=vmm_name
			dict_data["name"]=vmm_name
			dict_data["status"]="run"
			list_data.append(dict_data)
		return list_data



	#获取kvm的流量，内存，cpu等信息,返回以每个id为键值的字典，类似与列表，但方便储存
	def GetKvmInfo(self):
		conn = libvirt.open('qemu:///system') 
		dom = conn.listDomainsID() 
		data_id_dict={}
		for i in dom: 
			data_dict={}
			vmm_id = conn.lookupByID(i) 
			vmm_name = vmm_id.name() 
			vmm_id_str = str(vmm_name) 
			data_dict["id"]=vmm_id_str
			vmm_xml_name = vmm_id_str + '.' + 'xml' 
			vmm_xml_path = '/tmp/' + vmm_xml_name 
			vmm_xml_open = ET.parse(vmm_xml_path) 
			path_list=[] 
			path = vmm_xml_open.findall('.//source') 
			for i in path:
				file1 = i.attrib 
				filename=file1.get('file') 
				if filename: 
					path_list.append(filename) 
			 
			interface_list = [] 
			interface = vmm_xml_open.findall('.//target') 
			for j in interface: 
				interface_network = j.attrib 
				dev1 = interface_network.get('dev') 
				dev3 = 'vnet' 
				dev2 = str(dev1) 
				if dev3 in dev2: 
					interface_list.append(dev1) 	 



			 #获取流量信息
			totalrx_byte = 0 
			totaltx_byte = 0 
			for interfaceinfo_path in interface_list: 
				interfaceinfo = vmm_id.interfaceStats(interfaceinfo_path) 
				totalrx_byte = totalrx_byte + interfaceinfo[0] 
				totaltx_byte = totaltx_byte + interfaceinfo[4] 
			data_dict["net_input"]=float(totalrx_byte)/1024
			data_dict["net_output"]=float(totaltx_byte)/1024


			#获取cpu信息
			totalcpu =   'cpu'
			totalcpu_usage = 0 
			cpu_time =  vmm_id.info()[4] 
			data_dict["cpu_time"]=cpu_time




			#获取内存信息
			pid=(os.popen("ps aux|grep "+vmm_id_str+" | grep -v 'grep' | awk '{print $2}'").readlines()[0])
			memstatus=0
			#linux下 /proc/pid(进程ID）/smaps 下保存的是进程内存映像信息，比同一目录下的maps文件更详细些
			for line in file('/proc/%d/smaps' % int(pid),'r'):
				if re.findall('Private_',line):
				#统计Private内存信息量
					memstatus+=int(re.findall('(\d+)',line)[0])
			memusage=float('%.2f' % (int(memstatus)*100.0/int(vmm_id.info()[2])))-15
			if memusage>100.00:
				memusage=100.00
			elif memusage<0.00:
				memusage=0.00
			data_dict["mem"]=memusage
			data_id_dict[vmm_id_str]=data_dict

		return data_id_dict

		 



	#获取docker列表
	def GetDockerList(self):
		try:
			self.conn.request("GET", "/containers/json?all=1")
			r1 = self.conn.getresponse()
		except Exception,e:
				print traceback.format_exc()
				exit()
		raw = r1.read()
		data=json.loads(raw)
		list_data=[]
		#print data
		for item in data:
			dict_data={}
			# ltime=time.localtime(item["Created"])
			# dict_data["created_time"]=time.strftime("%Y-%m-%d %H:%M:%S", ltime)
			dict_data["id"]=item["Id"][0:12]
			dict_data["name"]=item["Names"][0].replace("/","")
			if "Up" in item["Status"]:
				dict_data["status"]="run"
			elif "Exited" in item["Status"]:
				dict_data["status"]="stop"
			else:
				dict_data["status"]="fault"
			list_data.append(dict_data)
		#print list_data
		return  list_data



	#计算kvm的cpu使用率
	def CalCpuUsage(self,old_data,now_data,t_diff):
		for kvm_id in now_data.keys():
			#若是新加入的kvm
			if kvm_id not in old_data.keys():
				now_data[kvm_id]["cpu"]=0.0
			else:
				cpu_time=(now_data[kvm_id]["cpu_time"]-old_data[kvm_id]["cpu_time"])/(t_diff*10000000)
				cpu_use=float('%0.2f'%cpu_time)
				if cpu_use>100.0:
					cpu_use=100
				now_data[kvm_id]["cpu"]=cpu_use

		return now_data		




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

		#流量数制转换(base on kB)
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



	#总监控程序入口
	def StatsMonitor(self):
		cmd = subprocess.Popen('sudo docker stats -a',stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
		stats_dict={}
		stats_dict_old={}
		stats_dict_old_kvm={}
		stats_dict_kvm={}
		t_start=datetime.datetime.now()
		update_count=0#计数，状态更新10次，进行一次id与name的添加删除操作
		host_list=self.GetKvmList()+self.GetDockerList()
		self.db.save_host_id_stats(host_list)
		while 1:
			stats_output = cmd.stdout.readline()
			stats_output=self.DelSerialSpace(stats_output)			
			stats=stats_output.split(" ")

			#获取bash每行信息
			if "CPU" not in stats:
				#print stats
				stats_parse=self.DockerStatsParse(stats)
				stats_dict[stats_parse["id"]]=stats_parse				

			#当全部获取完成时
			elif stats_dict!={}:
				#计算时间差

				t_end=datetime.datetime.now()
				diff=t_end-t_start
				t_start=t_end			
				t_diff=float(str(diff)[-8:])
				stats_dict_old=stats_dict
				stats_dict_kvm=self.GetKvmInfo()

				if stats_dict_old!={}:
					#计算网速
					stats_dict=self.CalFlowRate(stats_dict_old,stats_dict,t_diff)
					stats_dict_kvm=self.CalFlowRate(stats_dict_old_kvm,stats_dict_kvm,t_diff)
					stats_dict_kvm=self.CalCpuUsage(stats_dict_old_kvm,stats_dict_kvm,t_diff)
				else:
					stats_dict_old_kvm=stats_dict_kvm					
					stats_dict_kvm=self.CalFlowRate(stats_dict_old_kvm,stats_dict_kvm,t_diff)
					stats_dict_kvm=self.CalCpuUsage(stats_dict_old_kvm,stats_dict_kvm,t_diff)

				stats_dict_old=stats_dict
				stats_dict_old_kvm=stats_dict_kvm

				#sql操作,更新当前host状态
				result_flag_docker=self.db.save_host_stats(stats_dict)
				result_flag_kvm=self.db.save_host_stats(stats_dict_kvm)

				#每刷新10次，查询一下是否由新的host加入，是否有旧的host需要删除
				if update_count>10:
					#获取docker_list
					current_host_list=self.GetKvmList()+self.GetDockerList()

					#存储新加入的host
					self.db.save_host_id_stats(current_host_list)			

					#删除已失效的host		
					self.db.del_host_id_stats(current_host_list)

					#更新host的flag状态
					self.db.save_host_stats_flag(current_host_list)

					update_count=0

				update_count+=1
				print "状态数据更新！"
				#print stats_dict
				stats_dict={}

			



if __name__ == '__main__':
	demo=Monitor()
	demo.StatsMonitor()
