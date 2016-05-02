#coding=utf-8
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
	self.db_operate=DbOperate()

	

class TopoOperate(BaseOperate):
  """docstring for TopoOperate"""
  def __init__(self):
	#继承父类成员
	super(TopoOperate, self).__init__()


  def TopoCreate(self,data,config_file):

	#数据初始化
	network_topo=data["data"]["network_topo"]
	user_info=data["data"]["user_info"]

	config=config_file

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



	WriteTopoData(data)



if __name__ == '__main__':
	demo=TopoOperate()
	data=ReadTopoData()
	conf=ReadDockConf()
	demo.TopoCreate(data,conf)