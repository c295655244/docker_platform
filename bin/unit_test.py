#coding=utf-8
from topo_operate import *
from monitor import *


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



def test_db_save_host_id_stats():
	demo=Monitor()
	data_list=demo.GetDockerList()
	config=ReadDockConf()
	data=ReadTopoData("create")
	db=MysqlOperate(config)
	db.save_host_id_stats(data_list)

def test_monitor_stats():
	config=ReadDockConf()
	data=ReadTopoData("create")
	demo=MysqlOperate(config)


def test_insert():
	config=ReadDockConf()
	client=MySQLdb.connect(host=config["db_mysql"]["db_host"],user=config["db_mysql"]["db_user"],
		passwd=config["db_mysql"]["db_passwd"],db=config["db_mysql"]["db_database"],charset="utf8")
	cursor = client.cursor()
	host_tuple=("0.0","0.0","0.0","0.0","e695fc4e30d8")
	sql="UPDATE stats SET cpu=%s ,mem=%s,net_input=%s,net_output=%s   WHERE id = %s "%host_tuple
	print sql
	cursor.execute(sql)
	
	# 提交到数据库执行
	client.commit()
	client.close()



if __name__ == '__main__':
	
	#test_create_topo()
	#test_del_topo()
	test_insert()




