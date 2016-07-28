#coding=utf-8
import traceback  
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

	

class TopoOperate(BaseOperate):
  """docstring for TopoOperate"""
  def __init__(self):
	#继承父类成员
	super(TopoOperate, self).__init__()



  def TopoCreate(self,data):

  	config=self.conf

  	try:

		#数据初始化
		network_topo=data["data"]["network_topo"]
		user_info=data["data"]["user_info"]

		# 创建ovs网桥
		self.bridge_operate.OvsCreate(network_topo["link_list"],
			network_topo["network_core_list"])

		#创建docker
		network_topo["network_core_list"]=self.docker_operate.DockerCreate(config,
			network_topo["network_core_list"],
			user_info["user_id"])

		#kvm创建
		config,network_core_list=self.kvm_operate.KvmCreate(config,network_topo["network_core_list"],user_info["user_id"])


		network_topo["link_list"],network_topo["network_core_list"],host_data_list,router_data_list=\
		self.net_operate.NetConfig(network_topo["link_list"],
			network_topo["network_core_list"],
			config,user_info["user_id"])

		self.mongo_operate.save_dic(data,"cluster")
		data["data"]={}
		data["data"]["host_list"]=host_data_list
		data["data"]["router_list"]=router_data_list
		self.mongo_operate.save_dic(data,"host_list")
		

		data["status"]="success"
		data["msg"]="ok"
		
		#不能为空字符串，否则报错
		try:
			del data['_id']

		except:
			pass	
		WriteTopoData(data,"create")
		return data

  	except Exception, e:
  		data["status"]="error"
		data["msg"]=traceback.format_exc()
		data["data"]={}
  		print traceback.format_exc()
  		return data



  def TopoDelete(self,data):
  	config=self.conf
  	task_data={}
  	try:
  		
  		#查询拓扑
  		topo_dict=self.mongo_operate.get_data_condition("cluster",{"caseins":data["caseins"]})[0]
  		host_data=self.mongo_operate.get_data_condition("host_list",{"caseins":data["caseins"]})[0]
  		network_topo=topo_dict["data"]["network_topo"]
		user_info=topo_dict["data"]["user_info"]

		#删除kvm
		self.kvm_operate.KvmDel(host_data["data"]["host_list"])
		

  		#删除docker
  		self.docker_operate.DockerDel(config,user_info["user_id"])



  		# 删除ovs网桥
		self.bridge_operate.OvsDel(network_topo["link_list"],
			network_topo["network_core_list"])

		if debug =="false":
			self.mongo_operate.del_dict("cluster",{"caseins":data["caseins"]})
			self.mongo_operate.del_dict("host_list",{"caseins":data["caseins"]})
		data["status"]="success"
		data["msg"]="ok"
		data["data"]=topo_dict["data"]

		WriteTopoData(data,"del")
		return data
		


  	except Exception, e:
  		data["status"]="error"
		data["msg"]=traceback.format_exc()
		data["data"]={}
		print traceback.format_exc()
		return data



  #host监控api函数
  def Hostmonitor(self,data):
  	config=self.conf
  	data["data"]=[]
  	try:
  		for host_id in data["host_id"]:
  			{}
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
  		print data

  		WriteTopoData(data,"monitor_host")
		data["status"]="success"
		data["msg"]="ok"
  		return data
  	except Exception, e:
  		data["status"]="error"
		data["msg"]=traceback.format_exc()
		data["data"]=[]
		print traceback.format_exc()
		return data

  #docker 交互api函数
  def Hostmonitor(self,data):
  	config=self.conf
  	data["data"]=[]  	
  	




if __name__ == '__main__':
	pass