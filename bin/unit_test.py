#coding=utf-8
from topo_operate import *



#创建拓扑测试
def test_create_topo():
	demo=TopoOperate()
	data=ReadTopoData("create")
	demo.TopoCreate(data)

#删除拓扑测试
def test_del_topo():
	demo=TopoOperate()
	data=ReadTopoData("delete")
	demo.TopoDelete(data)


#创建网桥测试
def test_BridgeCreate():
	demo=BridgeOperate()
	data=ReadTopoData("create")
	conf=ReadDockConf()
	network_topo=data["data"]["network_topo"]
	user_info=data["data"]["user_info"]
	demo.OvsCreate(network_topo["link_list"],
		network_topo["network_core_list"])


#删除网桥测试
def test_BridgeDel():
	demo=BridgeOperate()
	data=ReadTopoData("create")
	conf=ReadDockConf()
	network_topo=data["data"]["network_topo"]
	user_info=data["data"]["user_info"]
	demo.OvsDel(network_topo["link_list"],
		network_topo["network_core_list"])


#配置网络测试
def test_NetConfig():
	demo=NetOperate()
	data=ReadTopoData("create")
	conf=ReadDockConf()
	docker_operate=DockerOperate()

	data["data"]["network_topo"]["network_core_list"]=docker_operate.DockerCreate(conf,data["data"]["network_topo"]["network_core_list"],
		data["data"]["user_info"]["user_id"])

	demo.NetConfig(data["data"]["network_topo"]["link_list"],
		data["data"]["network_topo"]["network_core_list"],
		conf,data["data"]["user_info"]["user_id"])	

#docker创建测试
def test_DockerCreate():
	demo=DockerOperate()
	data=ReadTopoData("create")
	conf=ReadDockConf()

	demo.DockerCreate(conf,data["data"]["network_topo"]["network_core_list"],
		data["data"]["user_info"]["user_id"])	


def test_DockerDel():
	demo=DockerOperate()
	data=ReadTopoData("create")
	conf=ReadDockConf()

	demo.DockerDel(conf,data["data"]["user_info"]["user_id"])	



if __name__ == '__main__':
	
	test_create_topo()


	test_del_topo()



