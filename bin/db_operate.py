#coding=utf-8
import sys,os,time
import traceback
import MySQLdb
from read_data import *
from pymongo import MongoClient
from set_log import *

class MongoOperate():

	def __init__(self,config):
		self.caseins="demo"
		self.logger=Logger()
		self.client = MongoClient(config["db_mongo"]["db_host"], 27017)
		self.database=config["db_mongo"]["db_database"]
		self.conf=config

		#用户认证需要依托一个存在的库，如admin
		self.client.admin.authenticate(config["db_mongo"]["db_user"], config["db_mongo"]["db_passwd"])



	'''
	@功能：lock操作，防止并发创建，选择唯一vnc端口
	'''
	def get_lock(self,timeout=10):
		flag=0
		data=self.client[self.database]["lock"]
		vnc_start=self.conf["host"]["vnc_start_port"]
		data_dic={
			"type":"lock",
			"vnc_start":vnc_start,
			"flag":0
		}
		count=0
		while 1:
			lock_info_list=[post for post in data.find({})]
			#print lock_info_list
			#若为第一次创建，自动采用配置文件的端口，获得锁
			if lock_info_list==[]:
				self.save_lock(data_dic,"lock")
				break
			else:
				#若当前用户正在创建，则等待
				if lock_info_list[0]["flag"]==0:
					print "其他用户正在操作，已等待"+str(count)+"秒..."
					time.sleep(1)
					count+=1
					#超时返回失败
					if count>=timeout:
						break
					continue

				#若当前空闲，获得锁
				else:
					flag=1
					data_dic["flag"]=0
					vnc_start=lock_info_list[0]["vnc_start"]
					data.delete_many({})
					self.save_lock(data_dic,"lock")
					break
		return flag,vnc_start



	def release_lock(self,vnc_start):
		data=self.client[self.database]["lock"]
		data_dic={
			"type":"lock",
			"vnc_start":vnc_start,
			"flag":1
		}
		data.delete_many({})
		self.save_lock(data_dic,"lock")






	'''
	@功能：存储操作
	'''	
	#存储模板
	def save_tpl_list(self,data_list,table,key=""):			
		data=self.client[self.database][table]
		if key=="":
			post_id = [data.insert_one(post).inserted_id  for post in data_list] 
			return post_id
		else:
			for post in data_list:
				if data.count({key:post[key]}) ==0:
					data.insert_one(post).inserted_id  

			#post_id = [data.insert_one(post).inserted_id  if data.count({key:post[key]}) !=0  for post in data_list]
			return data_list



	def save_dic(self,data_dic,table):
		data=self.client[self.database][table]
		data.delete_many({"caseins":data_dic["caseins"]})
		post_id = data.insert_one(data_dic).inserted_id 

	def save_lock(self,data_dic,table):
		data=self.client[self.database][table]
		post_id = data.insert_one(data_dic).inserted_id 

	def save_moniter_flag(self,data_dic,table):
		data=self.client[self.database][table]
		data.delete_many({"flag":data_dic["flag"]})
		post_id = data.insert_one(data_dic).inserted_id 


	'''
	@功能：读取操作
	'''
	def display_tpl(self,table):
		data=self.client[self.database][table]
		return [post for post in data.find({})]

	def get_data_condition(self,table,condition):
		data=self.client[self.database][table]
		return [post for post in data.find(condition)]



	def del_dict(self,table,condition):
		data=self.client[self.database][table]
		data.delete_many(condition)




class MysqlOperate():
	def __init__(self,config):
		self.client=MySQLdb.connect(
			host=config["db_mysql"]["db_host"],
			user=config["db_mysql"]["db_user"],
			passwd=config["db_mysql"]["db_passwd"],
			db=config["db_mysql"]["db_database"],
			charset="utf8")
		self.cursor = self.client.cursor()



	#全体查询模板
	def find_data(self,table):
		sql="select * from %s" %table
		self.cursor.execute(sql)
		results = self.cursor.fetchall() 
		return results	

	#查询host状态，供api函数使用
	def find_host_stats_api(self,host_id):
		sql="select * from stats where name='%s' " %host_id
		self.cursor.execute(sql)
		results = self.cursor.fetchone() 
		return results
		





	'''
	功能：stats表相关操作
	'''
	#检测该stats表中host条目是否存在
	def check_host_exist_stats(self,host_id,name):
		sql="select * from stats where id='%s' and name='%s' " %(host_id,name)
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		if results==[]:
			print host_id,name,"不存在!"


	#模糊查询host，不以real_id为键值
	#condition决定查找类型
	#condition=0，查找全部
	#condition=1，按host_id查找
	#condition=2，按router_id模糊查找
	def find_host_stats(self,condition=0,router_id="",host_id=""):
		if condition==0:
			sql="select * from stats "
		elif condition==1:
			router_id="%"+router_id+"%"
			sql="select * from stats where id like '%s'" % router_id
		else:
			sql="select * from stats where id = '%s' " % host_id

		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		data_dict={}
		for item in results:
			data_dict[item[0]]=item		
		return data_dict

	#提供全部搜索，以real_id为键值
	def find_host_stats_real_id(self):
		sql="select * from stats "
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		data_dict={}
		for item in results:
			data_dict[item[1]]=item		
		return data_dict

	#刷新数据库中stats标志
	def save_host_stats_flag(self,data_list):
		host_dict=self.find_host_stats(condition=0)
		host_list=[(item["status"],item["id"]) for item in data_list]
		host_tuple=tuple(host_list)
		try:
	
			sql="UPDATE stats SET stats=%s   WHERE id = %s "
			self.cursor.executemany(sql,host_tuple)
			# 提交到数据库执行
			self.client.commit()
			print "更新stats标志成功！"

		except Exception, e:
			print "更新状态出错！添加新id与name错误！"
			print traceback.format_exc()
			exit()



	#添加新的id与name
	def save_host_id_stats(self,data_list):
		host_dict=self.find_host_stats(condition=0)
		host_list=[(item["id"],item["name"],"0.0","0.0") for item in data_list if item["id"] not in host_dict.keys()]
		host_tuple=tuple(host_list)
		try:
			if host_tuple  != ():	
				sql="INSERT INTO stats(id,name,net_input,net_output)  VALUES (%s,%s,%s,%s) "
				self.cursor.executemany(sql,host_tuple)
				# 提交到数据库执行
				self.client.commit()
				print "添加新id以及name成功！"
			else:
				print "未有新host添加！"

		except Exception, e:
			print "更新状态出错！添加新id与name错误！"
			print traceback.format_exc()
			exit()



	#更新host状态
	def save_host_stats(self,data_dict):
		host_list=[(str(data_dict[key]["cpu"]),str(data_dict[key]["mem"]),
			data_dict[key]["id"]) for key in data_dict.keys()]
		host_tuple=tuple(host_list)
		sql="UPDATE stats SET cpu=%s ,mem=%s   WHERE id = %s "
		try:
			'''
			注意：若没有找到条目，此句不会报错！依然正常运行！
			'''
			self.cursor.executemany(sql,host_tuple)
			# 提交到数据库执行
			self.client.commit()

		except Exception, e:
			print "更新状态出错！"
			print traceback.format_exc()



	#删除已经失效的主机记录
	def del_host_id_stats(self,data_list):
		host_dict=self.find_host_stats(condition=0)
		data_dict=[item["id"] for item in data_list]
		host_list=[(host_dict[key][0],host_dict[key][1]) for key in host_dict.keys() if key not in data_dict]
		host_tuple=tuple(host_list)
		try:
			if host_tuple  != ():	
				sql="DELETE FROM stats WHERE id = %s and name=%s"
				self.cursor.executemany(sql,host_tuple)
				# 提交到数据库执行
				self.client.commit()
				print "删除旧id以及name成功！"
			else:
				print "未有旧host删除！"

		except Exception, e:
			print "更新状态出错！删除旧id以及name错误！"
			print traceback.format_exc()
			exit()


	#更新docker流量信息
	def save_docker_net_stats(self,data_dict):
		host_list=[(str(data_dict[key]["input_rate"]),str(data_dict[key]["output_rate"]),key
			) for key in data_dict.keys()]
		host_tuple=tuple(host_list)
		sql="UPDATE stats SET net_input=%s,net_output=%s  WHERE name = %s "
		try:
			'''
			注意：若没有找到条目，此句不会报错！依然正常运行！
			'''
			self.cursor.executemany(sql,host_tuple)
			# 提交到数据库执行
			self.client.commit()

		except Exception, e:
			print "更新状态出错！"
			print traceback.format_exc()		


	'''
	stats表操作结束
	'''






if __name__ == '__main__':
	config=ReadDockConf()
	demo=MongoOperate(config)
	demo.create_get_lock()
