#coding=utf-8
from topo_operate import *
from monitor import *
import copy
reload(sys)
sys.setdefaultencoding('utf-8')
def create(data):
	#记录已变更数据
	record={}
	record["user_id"]=copy.deepcopy(data["data"]["user_info"]["user_id"])
	data["data"]["user_info"]["user_id"]=record["user_id"][0:8]
	demo=TopoOperate()
	result=demo.TopoCreate(data)
	if result["status"]!="error":
		result["data"]["user_info"]["user_id"]=record["user_id"]
	return result

def delete(data):
	demo=TopoOperate()
	result=demo.TopoDelete(data)
	return result

def cmd(data):

	demo=TopoOperate()
	result=demo.HostCmd(data)
	
	return result

def monitor_host(data):
	demo=TopoOperate()
	result=demo.HostMonitor(data)
	return result

def monitor_topo(data):

	demo=TopoOperate()
	result=demo.TopoMonitor(data)
	
	return result



def monitor_cluster(data):

	demo=TopoOperate()
	result=demo.ClusterMonitor(data)
	
	return result



def log_day(data):

	demo=TopoOperate()
	result=demo.LogDay(data)
	
	return result


def log_month(data):

	demo=TopoOperate()
	result=demo.LogMonth(data)
	
	return result