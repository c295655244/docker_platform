#coding=utf-8
from topo_operate import *
from monitor import *
reload(sys)
sys.setdefaultencoding('utf-8')
def create(data):
	#记录已变更数据
	record={}
	record["user_id"]=data["data"]["user_info"]["user_id"]
	data["data"]["user_info"]["user_id"]=record["user_id"][0:8]
	demo=TopoOperate()
	result=demo.TopoCreate(data)
	data["data"]["user_info"]["user_id"]=record["user_id"]
	return result

def delete(delete_json):
	print delete_json
	result = {}
	#add code here
	
	return result

def cmd(cmd_json):
	print cmd_json
	result = {}
	#add code here
	
	return result

def moniter_host(moniter_host_json):
	print moniter_host_json
	result = {}
	#add code here
	
	return result

def moniter_topo(moniter_topo_json):
	print moniter_topo_json
	result = {}
	#add code here
	
	return result