#coding=utf-8
import sys,os
import MySQLdb
from read_data import *
from pymongo import MongoClient


class MongoOperate():

	def __init__(self,config):

		self.client = MongoClient(config["db_mongo"]["db_host"], 27017)
		self.database=config["db_mongo"]["db_database"]

		#用户认证需要依托一个存在的库，如admin
		self.client.admin.authenticate(config["db_mongo"]["db_user"], config["db_mongo"]["db_passwd"])


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
		data.delete_many({"topo_id":data_dic["topo_id"]})
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

		self.client=MySQLdb.connect(host=config["db_mysql"]["db_host"],user=config["db_mysql"]["db_user"],
			passwd=config["db_mysql"]["db_passwd"],db=config["db_mysql"]["db_database"],charset="utf8")
		self.cursor = self.client.cursor()



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


	#查询host
	#condition决定查找类型
	#condition=0，查找全部
	#condition=1，按host_id查找
	#condition=2，按router_id模糊查找
	def find_host_stats(self,condition=False,router_id="",host_id):
		if condition:
			sql="select * from stats "
		else:
			sql="select * from stats where id like '%lon%'"
		self.cursor.execute(sql)
		results = self.cursor.fetchall()
		data_dict={}
		for item in results:
			data_dict[item[0]]=item		
		return data_dict


	def save_host_id_stats(self,data_list):
		host_dict=find_all_host_stats()
		for item in data_list:
			if item["docker_id"] not in host_dict.keys():
				sql="INSERT INTO stats(id,name)"





if __name__ == '__main__':
	config=ReadDockConf()
	data=ReadTopoData("create")
	demo=MysqlOperate(config)