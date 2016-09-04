#coding=utf-8
import sys,os
import time,datetime
import yaml
import datetime
import subprocess 
import traceback
import signal
import copy 
from read_data import *
from set_log import *
exec_debug=ReadDockConf()["host"]["exec_debug"]
debug=ReadDockConf()["host"]["debug"]

class DockerOperate():
	"""docstring for DockerOperate"""
	def __init__(self):
		self.logger=Logger()
		self.caseins="demo"
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
			"services":{}
		}
		docker_temp={
			"image": "ubuntu:14.04",
			"network_mode": "none",
			"cpu_shares": 512,
			"cpuset": "0,1",
			"mem_limit": "512m",
			"expose":["80"],
			"privileged": True  
		}
		for count in xrange(len(network_core_list)):
			#为router标记id
			ids=network_core_list[count]["id"]
			router_id=str(user_id)+"_"+"router_"+ids+"_1"
			compose_file["services"]["router_"+ids]={
				"network_mode": "none",
				"privileged": True,
				
			}
			network_core_list[count]["docker_id"]=router_id
			docker_list=network_core_list[count]["host_type"]
			cluster_id=network_core_list[count]["id"]
			compose_file["services"]["router_"+ids]["image"]=network_core_list[count]["image"]
			if "router" in network_core_list[count]["image"]:
				compose_file["services"]["router_"+ids]["command"]="sleep 365d"


			#创建host的composefile
			for count_d in xrange(len(docker_list)):

				if docker_list[count_d]["type"]=="docker":
					docker_item=docker_list[count_d]
					docker_list[count_d]["compose_id"]=network_core_list[count]["id"]+"_"+str(count_d)
					docker_temp["image"]=docker_item["image"]
					docker_temp["cpuset"]=str(",".join([str(x) for x in xrange(int(docker_item["config"]["cpu_num"]))]))
					docker_temp["mem_limit"]=docker_item["config"]["mem"]


					#修改composefile
					compose_file["services"][cluster_id+"_"+str(count_d)]=copy.deepcopy(docker_temp)



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

		compose_cmd="sudo  docker-compose -f "+file_path+"  scale   "

		#存储网络核心的种类以及对应数量
		network_core_dict={}


		#添加docker主机创建命令
		for network_core in network_core_list:
			#添加网络核心创建命令
			router_create="router_"+network_core["id"]+"=1  "
			compose_cmd+=router_create


			#统计各docker集群数量
			for cluster in network_core["host_type"]:
				if cluster["type"]=="docker":
					cmd_tmp=cluster["compose_id"]+"="+str(cluster["host_num"])+"   "
					compose_cmd+=cmd_tmp



		if debug =="false":
			os.system(compose_cmd)
		self.logger.log_save(compose_cmd,self.caseins,"info")
		#print compose_cmd

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

		self.logger.log_save(compose_cmd_stop,self.caseins,"info")		
		self.logger.log_save(compose_cmd_rm,self.caseins,"info")

		#print compose_cmd_stop
		#print compose_cmd_rm




	#为docker下达命令
	#flag=1 只进行单条执行，返回信息
	#flsg=0 只进行批量执行,不返回信息
	def DockerCmd(self,docker_id,cmd,timeout=5,flag=0):
		exec_cmd="sudo docker exec %s  %s"%(docker_id,cmd)
		exec_cmd_many="sudo docker exec  -d  %s  %s"%(docker_id,cmd)
		timeout-=1
		print exec_cmd
		try: 
			if exec_debug =="false":
				start = datetime.datetime.now()		
				if flag==1:
					proc = subprocess.Popen(exec_cmd,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)	
					self.logger.log_save("主机"+docker_id+"运行命令："+cmd,self.caseins,"info")
					while proc.poll() is None:
						time.sleep(0.1)
						now = datetime.datetime.now()
						if (now - start).seconds> timeout:
							os.kill(proc.pid, signal.SIGKILL)
							os.waitpid(-1, os.WNOHANG)
							return None
					out=proc.stdout.read()
					self.logger.log_save("主机"+docker_id+"返回命令："+out,self.caseins,"info")		
					return out
				else:
					proc = subprocess.Popen(exec_cmd_many,stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)	
					self.logger.log_save("主机"+docker_id+"批量运行命令："+cmd,self.caseins,"info")					
					return True
			else:
				return "此数据为测试数据！"
		except Exception, e:
			print traceback.format_exc()
			return str(traceback.format_exc())

	
