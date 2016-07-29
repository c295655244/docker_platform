#coding=utf-8
import sys,os
import time,datetime
import yaml
import datetime
import subprocess 
import traceback
import signal
from read_data import *
debug=ReadDockConf()["host"]["debug"]

class DockerOperate():
	"""docstring for DockerOperate"""
	def __init__(self):
		pass


	#检查是否存在对应的用户文件
	def CheckUserFile(self,config,user_id):
		file_path=config["host"]["compose_file_path"]+"user/"+str(user_id)
		if not os.path.exists(file_path):
			os.makedirs(file_path)

	#创建compose文件，默认网络设备全为路由器
	#添加各路由下的集群id
	def ComfileCreate(self,config,network_core_list,user_id):
		file_path=config["host"]["compose_file_path"]+"user/"+str(user_id)+"/docker-compose.yaml"
		self.CheckUserFile(config,user_id)

		file_yaml=open(file_path,'w')
		compose_file={
			"version":"2",
			"services":{
				"router":{
					"image": "ubuntu:14.04",
					"command": "sleep 365d",
					"network_mode": "none",
					"privileged": True
				}
			}
		}
		docker_temp={
			"image": "ubuntu:14.04",
			"command": "sleep 365d",
			"network_mode": "none",
			"cpu_shares": 512,
			"cpuset": "0,1",
			"mem_limit": "512m",
			"privileged": True  
		}
		for count in xrange(len(network_core_list)):
			#为router标记id
			router_id=str(user_id)+"_"+network_core_list[count]["type"]+"_"+str(count+1)
			network_core_list[count]["docker_id"]=router_id
			docker_list=network_core_list[count]["host_type"]
			cluster_id=network_core_list[count]["id"]

			#创建host的composefile
			for count_d in xrange(len(docker_list)):

				if docker_list[count_d]["type"]=="docker":
					docker_item=docker_list[count_d]
					docker_temp["image"]=docker_item["image"]
					docker_temp["cpuset"]=",".join([str(x) for x in xrange(int(docker_item["config"]["cpu_num"]))])
					docker_temp["mem_limit"]=docker_item["config"]["mem"]


					#修改composefile
					compose_file["services"][cluster_id+"_"+str(count_d)]=docker_temp


		#print network_core_list,file_path

		#此句防止出现!!python/unicode串
		yaml.add_representer(unicode, lambda dumper, 
						value: dumper.represent_scalar(u'tag:yaml.org,2002:str', value))

		#写入yaml
		yaml.dump(compose_file,file_yaml,allow_unicode=True,
						 default_flow_style=False)
		file_yaml.close()

		return network_core_list,file_path


	def DockerCreate(self,config,network_core_list,user_id):

		#创建complie-file
		network_core_list,file_path=self.ComfileCreate(config,network_core_list,user_id)

		compose_cmd="sudo  docker-compose -f "+file_path+"  scale  "

		#存储网络核心的种类以及对应数量
		network_core_dict={}


		#添加docker主机创建命令
		for network_core in network_core_list:

			#按种类统计网络核心数量，例如router=3
			if not network_core_dict.has_key(network_core["type"]):
				network_core_dict[network_core["type"]]=1
			else:
				network_core_dict[network_core["type"]]+=1

			#统计各docker集群数量
			for cluster in network_core["host_type"]:
				if cluster["type"]=="docker":
					cmd_tmp=cluster["id"]+"="+str(cluster["host_num"])+"   "
					compose_cmd+=cmd_tmp


		#添加网络核心创建命令
		for (net_name,num) in network_core_dict.items():
			cmd_tmp=net_name+"="+str(num)+"   "
			compose_cmd+=cmd_tmp 

		if debug =="false":
			os.system(compose_cmd)
		print compose_cmd

		return network_core_list



	def DockerDel(self,config,user_id):
		#创建complie-file
		file_path=config["host"]["compose_file_path"]+"user/"+str(user_id)+"/docker-compose.yaml"


		compose_cmd_pre="sudo  docker-compose -f "+file_path

		compose_cmd_stop=compose_cmd_pre+"  stop"

		compose_cmd_rm=compose_cmd_pre+"  rm  -f"

		if debug =="false":
			os.system(compose_cmd_stop)
			os.system(compose_cmd_rm)


		print compose_cmd_stop
		print compose_cmd_rm




	#为docker下达命令
	#flag=0 只进行单条执行，返回信息
	#flsg=1 只进行批量执行,不返回信息
	def DockerCmd(self,docker_id,cmd,timeout=5,flag=0):
		exec_cmd="sudo docker exec %s  %s"%(docker_id,cmd)
		timeout-=1
		print exec_cmd
		try: 
			start = datetime.datetime.now()
			proc = subprocess.Popen(exec_cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)	
			if flag==1:
				while proc.poll() is None:
					time.sleep(0.1)
					now = datetime.datetime.now()
					if (now - start).seconds> timeout:
						os.kill(proc.pid, signal.SIGKILL)
						os.waitpid(-1, os.WNOHANG)
						return None
				return proc.stdout.read()
			else:
				return True
		except Exception, e:
			print traceback.format_exc()
			return str(traceback.format_exc())

	
