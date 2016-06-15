#! /usr/bin/env python
#-*-coding:utf-8-*-
import sys
import subprocess 
import datetime



class Monitor(object):

	#去除多余空格		
	def DelSerialSpace(self,str_data):
		while str_data.find("  ")!=-1:
			str_data=str_data.replace('  ',' ')
		return str_data

	#格式化数据
	def DockerStatsParse(self,data):
		data_dict={}	
		data_dict["docker_id"]=data[0]
		data_dict["cpu"]=float(data[1].replace("%",""))
		data_dict["men"]=float(data[7].replace("%",""))

		#流量数制转换
		if data[9]=="B":
			data_dict["net_input"]=0.0
		elif data[9]=="MB":
			data_dict["net_input"]=float(data[8])*1024
		elif data[9]=="GB":
			data_dict["net_input"]=float(data[8])*1024*1024
		else:
			data_dict["net_input"]=float(data[8])

		if data[12]=="B":
			data_dict["net_output"]=0.0
		elif data[12]=="MB":
			data_dict["net_output"]=float(data[11])*1024
		elif data[12]=="GB":
			data_dict["net_output"]=float(data[11])*1024*1024
		else:
			data_dict["net_output"]=float(data[11])

		return data_dict


	#计算流量速度
	def CalFlowRate(self,old_data,now_data,t_diff):
		for docker_id in now_data.keys():
			#若是新加入的docker
			if docker_id not in old_data.keys():
				now_data[docker_id]["input_rate"]=0
				now_data[docker_id]["output_rate"]=0
			else:
				input_rate=(now_data[docker_id]["net_input"]-old_data[docker_id]["net_input"])/t_diff
				output_rate=(now_data[docker_id]["net_output"]-old_data[docker_id]["net_output"])/t_diff
				now_data[docker_id]["input_rate"]=int(input_rate)
				now_data[docker_id]["output_rate"]=int(output_rate)
				print input_rate,output_rate

		# old_data["net_input"]
		# old_data["net_input_unit"]



	def DockerMonitor(self):
		cmd = subprocess.Popen('sudo docker stats -a',stdin=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)
		stats_dict={}
		stats_dict_old={}	
		t_start=datetime.datetime.now()
		while 1:
			stats_output = cmd.stdout.readline()
			stats_output=self.DelSerialSpace(stats_output)
			stats=stats_output.split(" ")

			if "CPU" not in stats:
				stats_parse=self.DockerStatsParse(stats)
				stats_dict[stats_parse["docker_id"]]=stats_parse

			elif stats_dict!={}:
				#计算时间差
				t_end=datetime.datetime.now()
				diff=t_end-t_start
				t_start=t_end
				t_diff=float(str(diff)[-8:])

				if stats_dict_old!={}:
					self.CalFlowRate(stats_dict_old,stats_dict,t_diff)

				stats_dict_old=stats_dict

				pass#sql操作,存储状态
				print "状态数据更新！"
				print stats_dict
				stats_dict={}


if __name__ == '__main__':
	demo=Monitor()
	demo.DockerMonitor()
