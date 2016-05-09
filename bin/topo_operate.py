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
	self.db_operate=DbOperate(self.conf)

	

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
		self.kvm_operate.KvmCreate()


		network_topo["link_list"],network_topo["network_core_list"]=\
		self.net_operate.NetConfig(network_topo["link_list"],
			network_topo["network_core_list"],
			config,user_info["user_id"])

		
		self.db_operate.save_dic(data,"cluster")


		data["status"]="success"
		data["msg"]="ok"
		#不能为空字符串，否则报错
		del data['_id']

		WriteTopoData(data,"create")

		return True

  	except Exception, e:
  		data["status"]="fail"
		data["msg"]=traceback.format_exc()
		data["data"]={}
  		print traceback.format_exc()
  		return False



  def TopoDelete(self,data):
  	config=self.conf
  	task_data={}
  	try:
  		#查询拓扑
  		topo_dict=self.db_operate.get_data_condition("cluster",{"topo_id":data["topo_id"]})[0]

  		network_topo=topo_dict["data"]["network_topo"]
		user_info=topo_dict["data"]["user_info"]


  		#删除docker
  		self.docker_operate.DockerDel(config,user_info["user_id"])


  		# 删除ovs网桥
		self.bridge_operate.OvsDel(network_topo["link_list"],
			network_topo["network_core_list"])


		self.db_operate.del_dict("cluster",{"topo_id":data["topo_id"]})

		data["status"]="success"
		data["msg"]="ok"
		data["data"]=topo_dict["data"]


		WriteTopoData(data,"del")

		return True


  	except Exception, e:
  		data["status"]="fail"
		data["msg"]=traceback.format_exc()
		data["data"]={}
		print traceback.format_exc()






if __name__ == '__main__':
	pass