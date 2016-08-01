#coding=utf-8
import sys,os
from read_data import *
from set_log import *


debug=ReadDockConf()["host"]["debug"]



class BridgeOperate():
	"""docstring for BridgeOperate"""

	def __init__(self):
		self.caseins="demo"
		self.logger=Logger()
		pass

	def check_dup_link(link_list):
		pass


	def OvsDel(self,link_list,network_core_list):
		core_num=len(network_core_list)
		#adjacent_matrix=self.CreateRelationMatrix(link_list,core_num)

		#创建路由间网桥
		for link_relation in link_list:
			bridge_name="br_router_"+str(link_relation["link"][0])+"_"+str(link_relation["link"][1])
			self.BridgeDel(bridge_name)

		#创建主机间网桥
		for switch_host in network_core_list:
			if switch_host["host_num"]>0:
				bridge_name="br_"+switch_host["id"]
				self.BridgeDel(bridge_name)


	def OvsCreate(self,link_list,network_core_list):
		core_num=len(network_core_list)

		#创建路由间网桥
		for link_relation in link_list:
			bridge_name="br_router_"+str(link_relation["link"][0])+"_"+str(link_relation["link"][1])
			self.BridgeCreate(bridge_name)

		#创建主机间网桥
		for switch_host in network_core_list:
			bridge_name="br_"+switch_host["id"]
			self.BridgeCreate(bridge_name)



	def BridgeCreate(self,bridge_name):

		cmd='sudo ovs-vsctl add-br %s' %bridge_name

		if debug =="false":		
			os.system(cmd)

		self.logger.log_save(cmd,self.caseins,"info")
		#print  cmd

	def BridgeDel(self,bridge_name):

		cmd='sudo ovs-vsctl del-br %s' %bridge_name
		if debug =="false":		
			os.system(cmd)
		self.logger.log_save(cmd,self.caseins,"info")
		#print  cmd


