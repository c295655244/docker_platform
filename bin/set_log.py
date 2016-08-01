#coding:utf8
import sys,os
import time
from read_data import *
import calendar
reload(sys)
sys.setdefaultencoding('utf-8')

class Logger():

	"""docstring for DockerOperate"""
	def __init__(self):
		pass

	def log_save(self,msg,caseins,rank):
		conf=ReadDockConf()
		current_day=str(time.strftime("%Y-%m-%d",time.localtime(time.time())))
		current_time=str(time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time())))
		dir_path=conf["host"]["log_path"]+current_day
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)
		log_path=dir_path+"/"	+caseins+".log"
		file_object = open(log_path, 'a')
		str_conf="["+current_time+"] <"+rank+">  "+msg
		print str_conf
		file_object.write(str_conf)
		file_object.write("\n")
		file_object.close( )

	def cul_day_num(self,month):
		date=month.split("-")
		return  calendar.monthrange(int(date[0]),int(date[1]))[1]



if __name__ == '__main__':
	demo=Logger()
	demo.log_save('this is test!',"21asd56wad1","info")
	demo.cul_day_num("2016-08")