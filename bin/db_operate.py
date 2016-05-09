#coding=utf-8
import sys,os
from read_data import *
from pymongo import MongoClient


class DbOperate():

	def __init__(self,config):

		self.client = MongoClient(config["db"]["db_host"], 27017)
		self.database=config["db"]["db_database"]

		#用户认证需要依托一个存在的库，如admin
		self.client.admin.authenticate(config["db"]["db_user"], config["db"]["db_pass"])


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


if __name__ == '__main__':
	config=ReadDockConf()
	data=ReadTopoData("create")
	demo=DbOperate(config)
	demo.save_dic(data,"cluster")