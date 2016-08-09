#coding=utf-8
import traceback  
import logging  
import logging.handlers
from set_log import *
from read_data import *
from db_operate import *
from kvm_operate import *
from bridge_operate import *
from docker_operate import *
from net_operate import *


reload(sys)
sys.setdefaultencoding('utf-8')

debug=ReadDockConf()["host"]["debug"]


class BaseOperate(object):
	"""docstring for BaseOperate"""
	def __init__(self):
		self.conf=ReadDockConf()
		self.bridge_operate=BridgeOperate()
		self.docker_operate=DockerOperate()
		self.kvm_operate=KvmOperate()
		self.net_operate=NetOperate()
		self.mongo_operate=MongoOperate(self.conf)
		self.mysql_operate=MysqlOperate(self.conf)
		self.logger=Logger()

	

class TopoOperate(BaseOperate):
	"""docstring for TopoOperate"""
	def __init__(self):
	#继承父类成员
		super(TopoOperate, self).__init__()



	def TopoCreate(self,data):

		config=self.conf
		caseins=data["caseins"]
		#获取创建锁
		create_flag,vnc_start= self.mongo_operate.get_lock()
		try:
			if create_flag==0:
				data["status"]="error"
				data["msg"]="获得锁失败！其他用户正在操作！"
				self.logger.log_save("获得锁失败！其他用户正在操作！",caseins,"error")
				print "获得锁失败！其他用户正在操作！"
				return data
			config["host"]["vnc_start_port"]=vnc_start
			print "获得锁成功！开始创建！"

			self.bridge_operate.caseins=caseins
			self.docker_operate.caseins=caseins
			self.kvm_operate.caseins=caseins
			self.net_operate.caseins=caseins

			user_data=data["data"]["user_info"]
			

			#数据初始化
			network_topo=data["data"]["network_topo"]
			user_info=data["data"]["user_info"]

			self.logger.log_save('数据初始化完成!',caseins,"info")

			#print "数据初始化完成!"

			# 创建ovs网桥
			self.bridge_operate.OvsCreate(network_topo["link_list"],
				network_topo["network_core_list"])

			self.logger.log_save('网桥创建完成!',caseins,"info")
			#print "网桥创建完成"

			#创建docker
			network_topo["network_core_list"]=self.docker_operate.DockerCreate(config,
				network_topo["network_core_list"],
				user_info["user_id"])

			self.logger.log_save('docker创建完成!',caseins,"info")			
			#print "docker创建完成!"

			#kvm创建
			config,network_core_list=self.kvm_operate.KvmCreate(config,network_topo["network_core_list"],user_info["user_id"])
			self.logger.log_save('kvm创建完成!',caseins,"info")
			#print "kvm创建完成!"

			network_topo["link_list"],network_topo["network_core_list"],host_data_list,router_data_list=\
			self.net_operate.NetConfig(network_topo["link_list"],
				network_topo["network_core_list"],
				config,user_info["user_id"])
			self.logger.log_save('网络配置完成!',caseins,"info")
			#print "网络配置完成！"
			self.kvm_operate.VncAdd(config,host_data_list)
			self.logger.log_save('添加vnc设置完成!',caseins,"info")
			self.mongo_operate.save_dic(data,"cluster")

			data["data"]={}
			data["data"]["user_info"]=user_data
			data["data"]["host_list"]=host_data_list
			data["data"]["router_list"]=router_data_list


			self.mongo_operate.save_dic(data,"host_list")
			self.logger.log_save('数据库存储完成!',caseins,"info")
			#print "数据库存储完成!"

			#释放锁
			self.mongo_operate.release_lock(config["host"]["vnc_start_port"])

			data["status"]="success"
			data["msg"]="ok"
		
			#不能为空字符串，否则报错
			try:
				del data['_id']
			except:
				pass 

			WriteTopoData(data,"create")
			self.logger.log_save('拓扑创建成功!',caseins,"info")
			#print "拓扑创建成功!"
			return data

		except Exception, e:
			data["status"]="error"
			data["msg"]=traceback.format_exc()
			#释放锁
			self.mongo_operate.release_lock(vnc_start)
			self.logger.log_save(str(traceback.format_exc()),caseins,"error")
			print traceback.format_exc()
			return data




	#拓扑删除
	def TopoDelete(self,data):
		config=self.conf
		task_data={}
		caseins=data["caseins"]
		try:
			#获取删除锁
			create_flag,vnc_start= self.mongo_operate.get_lock()
			if create_flag==0:
				data["status"]="error"
				data["msg"]="获得锁失败！其他用户正在操作！"
				self.logger.log_save("获得锁失败！其他用户正在操作！",caseins,"error")
				print "获得锁失败！其他用户正在操作！"
				return data
			config["host"]["vnc_start_port"]=vnc_start
			print "获得锁成功！开始删除！"

			self.bridge_operate.caseins=caseins
			self.docker_operate.caseins=caseins
			self.kvm_operate.caseins=caseins
			self.net_operate.caseins=caseins						
			#查询拓扑
			topo_dict=self.mongo_operate.get_data_condition("cluster",{"caseins":data["caseins"]})[0]
			host_data=self.mongo_operate.get_data_condition("host_list",{"caseins":data["caseins"]})[0]
			network_topo=topo_dict["data"]["network_topo"]
			user_info=topo_dict["data"]["user_info"]

			#删除kvm
			self.kvm_operate.KvmDel(host_data["data"]["host_list"])
			self.logger.log_save('删除kvm完成!',caseins,"info")	

			#删除docker
			self.docker_operate.DockerDel(config,user_info["user_id"])
			self.logger.log_save('删除docker完成!',caseins,"info")

			#删除ovs网桥
			self.bridge_operate.OvsDel(network_topo["link_list"],
				network_topo["network_core_list"])
			self.logger.log_save('删除ovs网桥完成!',caseins,"info")

			#删除vnc设置
			self.kvm_operate.VncDel(config,host_data["data"]["host_list"])	
			self.logger.log_save('删除vnc端口完成!',caseins,"info")


			if debug =="false":
				pass
				#self.mongo_operate.del_dict("cluster",{"caseins":data["caseins"]})
				#self.mongo_operate.del_dict("host_list",{"caseins":data["caseins"]})

			data["status"]="success"
			data["msg"]="ok"
			data["data"]=topo_dict["data"]

			#释放锁
			self.mongo_operate.release_lock(vnc_start)

			WriteTopoData(data,"del")
			#print "删除拓扑成功!"
			return data
		


		except Exception, e:
			data["status"]="error"
			data["msg"]=traceback.format_exc()
			data["data"]={}
			#释放锁
			self.mongo_operate.release_lock(config["host"]["vnc_start_port"])
			self.logger.log_save(str(traceback.format_exc()),caseins,"error")
			print traceback.format_exc()
			return data



	#host监控api函数
	def HostMonitor(self,data):
		config=self.conf
		data["data"]=[]
		docker_list_flag={
			"flag":"monitor_flag",
			"docker_list":[]
		}
		try:
			for host_id in data["host_id"]:
				item_data=self.mysql_operate.find_host_stats_api(host_id)
				if item_data!=None:
					item={
					"host_id": item_data[1],
					"cpu": item_data[2],
					"mem": item_data[3],
					"net_input": item_data[4],
					"net_output": item_data[5],
					"stats": item_data[6]
					}
					data["data"].append(item)
					docker_list_flag["docker_list"].append(item_data[1])
				else:
					item={
						"host_id":host_id,
						"cpu": 0.0,
						"mem":0.0 ,
						"net_input":0.0 ,
						"net_output": 0.0,
						"stats":"stop"
					}
					data["data"].append(item)
			self.mongo_operate.save_moniter_flag(docker_list_flag,"monitor_flag")
			#print data
			WriteTopoData(data,"monitor_host")
			data["status"]="success"
			data["msg"]="ok"
			print "主机状态查询成功!"
			return data
		except Exception, e:
			data["status"]="error"
			data["msg"]=traceback.format_exc()
			data["data"]=[]
			print traceback.format_exc()
			return data



	#docker 交互api函数
	def HostCmd(self,data):
		config=self.conf
		data["data"]=[]
		caseins=data["caseins"]		
		timeout=int(config["host"]["cmd_timeout"])
		out_str=""
		try:
			self.docker_operate.caseins=caseins
			self.logger.log_save("拓扑"+caseins+"执行指令"+data["cmd"],caseins,"info")
			if len(data["host_id"])==1:
				out_str=self.docker_operate.DockerCmd(data["host_id"][0],data["cmd"],timeout=timeout,flag=1)
			else:
				for host_id in data["host_id"]:
					out_str=self.docker_operate.DockerCmd(host_id,data["cmd"],timeout=timeout,flag=0)

			data["status"]="success"
			data["msg"]="ok"
			data["data"]={
				"return": out_str
			}
			#print data
			self.logger.log_save("执行指令成功！",caseins,"info")
			print "命令执行成功!"
			return data
		except Exception, e:
			data["status"]="error"
			data["msg"]=traceback.format_exc()
			data["data"]=[]
			self.logger.log_save(str(traceback.format_exc()),caseins,"error")
			print traceback.format_exc()
			return data


	def TopoMonitor(self,data):
		try:		
			save_data=self.mongo_operate.get_data_condition("host_list",{"caseins":data["caseins"]})[0]
			run_host_data=self.mysql_operate.find_host_stats_real_id()
			router_list=[ item["real_id"]   for item in  save_data["data"]["router_list"]]
			host_list=[ item["real_id"]   for item in  save_data["data"]["host_list"]]
			host_data=router_list+host_list
			run=0
			stop=0
			fault=0
			for host_id in host_data:

				if host_id in run_host_data.keys():
					if run_host_data[host_id][6] == "run":
						run+=1
					else:
						stop+=1
				else: 
					fault+=1
			data["status"]="success"
			data["msg"]="ok"
			data["data"]={
				"run_num":run,
				"stop_num":stop,
				"fault_num":fault
			}
			#print data
			print "拓扑状态查询成功!"
			return data
		except Exception, e:
			data["status"]="error"
			data["msg"]=traceback.format_exc()
			data["data"]=[]
			print traceback.format_exc()
			return data



	def ClusterMonitor(self,data):
		try:		
			run_host_data=self.mysql_operate.find_host_stats_real_id()
			host_data=data["host_id"]
			run=0
			stop=0
			fault=0
			for host_id in host_data:
				if host_id in run_host_data.keys():
					if run_host_data[host_id][6] == "run":
						run+=1
					else:
						stop+=1
				else: 
					fault+=1
			data["status"]="success"
			data["msg"]="ok"
			data["data"]={
				"run_num":run,
				"stop_num":stop,
				"fault_num":fault
			}

			#print data
			print "集群状态查询成功!"
			return data
		except Exception, e:
			data["status"]="error"
			data["msg"]=traceback.format_exc()
			data["data"]=[]
			print traceback.format_exc()
			return data


	def LogAll(self,data):
		try:			
			config=self.conf
			caseins=data["caseins"]
			dir_path=config["host"]["log_path"]
			list_dir=os.listdir(dir_path)
			data_list=[]
			for date in list_dir:
				log_path=dir_path+date+"/"+caseins+".log"
				#print log_path
				if os.path.exists(log_path):
					data_list.append(date)
			data["status"]="success"
			data["msg"]="ok"
			data["data"]=data_list
			print "当月日志查询成功!"
			return data			
		except Exception, e:
			data["status"]="error"
			data["msg"]=str(traceback.format_exc())
			data["data"]=[]
			print traceback.format_exc()
			return data
		

	def LogDay(self,data):
		try:			
			config=self.conf
			caseins=data["caseins"]
			date=data["date"]
			dir_path=config["host"]["log_path"]
			log_url=config["host"]["log_url"]
			log_path=dir_path+date+"/"+caseins+".log"
			if not os.path.exists(log_path):
				is_exist=0
				url=""
			else:
				is_exist=1
				url=log_url+date+"/"+caseins+".log"
			data["status"]="success"
			data["msg"]="ok"
			data["data"]={
				"is_exist":is_exist,
				"url":url
			}
			print "当日日志查询成功!"
			return data	
		except Exception, e:
			data["status"]="error"
			data["msg"]=str(traceback.format_exc())
			data["data"]=[]
			print traceback.format_exc()
			return data

	def Vnc(self,data):
		try:			
			config=self.conf
			caseins=data["caseins"]
			host_id=data["real_id"]
			url=config["host"]["vnc_url"]+host_id
			data["status"]="success"
			data["msg"]="ok"
			data["data"]={
				"url":url
			}
			print "VNC查询成功!"
			return data	
		except Exception, e:
			data["status"]="error"
			data["msg"]=str(traceback.format_exc())
			data["data"]=[]
			print traceback.format_exc()
			return data		


	def GetImage(self,data):
		try:
			result=self.mysql_operate.find_data("images")
			data_list=[]
			for item in result:
				item_dict={
					"image_name":item[0],
					"hot_num":item[2],
					"use_num":item[1],
					"image_url":item[3],
					"type":item[4]
				}
				data_list.append(item_dict)
			data["status"]="success"
			data["msg"]="ok"
			data["data"]={
				"image_list":data_list
			}
			data_list
			print "镜像查询成功!"
			return data
		except Exception, e:
			data["status"]="error"
			data["msg"]=str(traceback.format_exc())
			data["data"]=[]
			print traceback.format_exc()
			return data

if __name__ == '__main__':
	pass