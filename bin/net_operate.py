#coding=utf-8
import sys,os
from heapq import *
from read_data import *
from collections import defaultdict
from docker_operate import *
from set_log import *

debug=ReadDockConf()["host"]["debug"]

reload(sys)
sys.setdefaultencoding('utf-8')





class NetOperate():
	"""docstring for BridgeOperate"""

	def __init__(self):
		self.caseins="demo"
		self.logger=Logger()
		pass


	def ip2num(self,ip):
		ip=[int(x) for x in ip.split('.')]
		return ip[0] <<24 | ip[1]<<16 | ip[2]<<8 |ip[3]


	def num2ip(self,num):
		return '%s.%s.%s.%s' %( (num & 0xff000000) >>24,
			(num & 0x00ff0000) >>16,
			(num & 0x0000ff00) >>8,
			num & 0x000000ff )
	#计算掩码
	def cul_mask(self,mask_num):
		return self.num2ip(0xffffffff << (32-mask_num))


	#ip加num
	def IpAdd(self,ip,num):
		return self.num2ip(self.ip2num(ip)+num)




	#向单个docker添加ip
	def IpConfigDocker(self,host_dict,docker_id_pre,ip,num,bridge,gateway_ip):
		docker_data_list=[]
		bridge_id="br_"+bridge
		for count in xrange(num):

			'''
			此处分配ip，连接网桥
			'''
			docker_id =docker_id_pre+str(count+1)

			if debug =="false":
				os.system("sudo ovs-docker add-port %s eth0 %s"%(bridge_id,docker_id))
				os.system("sudo docker exec %s ifconfig eth0 %s/24"%(docker_id,ip))
				os.system("sudo docker exec %s route add default gw %s"%(docker_id,gateway_ip))
			cmd1= "sudo ovs-docker add-port %s eth0 %s"%(bridge_id,docker_id)
			cmd2="sudo docker exec %s ifconfig eth0 %s/24"%(docker_id,ip)
			cmd3="sudo docker exec %s route add default gw %s"%(docker_id,gateway_ip)

			self.logger.log_save(cmd1,self.caseins,"info")
			self.logger.log_save(cmd2,self.caseins,"info")
			self.logger.log_save(cmd3,self.caseins,"info")
			#print "sudo ovs-docker add-port %s eth0 %s"%(bridge_id,docker_id)
			#print "sudo docker exec %s ifconfig eth0 %s/24"%(docker_id,ip)
			#print "sudo docker exec %s route add default gw %s"%(docker_id,gateway_ip)
			save_data={
				"real_id": docker_id,
				"router_id":bridge,
				"cluster_id":host_dict["id"],
				"image": host_dict["image"],
				"type": "docker",
				"config": {
					"cpu_num": host_dict["config"]["cpu_num"],
					"mem": host_dict["config"]["mem"]
					},
				"bridge": bridge_id,
				"vncport": 0,
				"ip":ip
			}
			docker_data_list.append(save_data)
			ip=self.IpAdd(ip,1)

			#print docker_id_pre+str(count+1)+"  主机配ip: "+ip+"  连接网桥:"+bridge_id
		return ip,docker_data_list


	#向router添加ip
	def IpConfigRouter(self,docker_id,ip,bridge_id,mac_name,mask):

		'''
		此处分配ip，连接网桥
		'''
		if debug =="false":
			os.system("sudo ovs-docker add-port %s %s %s"%(bridge_id,mac_name,docker_id))
			os.system("sudo docker exec %s ifconfig %s %s/%s"%(docker_id,mac_name,ip,str(mask)))


		cmd1= "sudo ovs-docker add-port %s %s %s"%(bridge_id,mac_name,docker_id)
		cmd2= "sudo docker exec %s ifconfig %s %s/%s"%(docker_id,mac_name,ip,str(mask))	

		self.logger.log_save(cmd1,self.caseins,"info")
		self.logger.log_save(cmd2,self.caseins,"info")
		#print "sudo ovs-docker add-port %s %s %s"%(bridge_id,mac_name,docker_id)
		#print "sudo docker exec %s ifconfig %s %s/%s"%(docker_id,mac_name,ip,str(mask))	




	#向路由器节点配置路由表命令
	def RouterAdd(self,router_id,dst_ip,mask,forward_ip):
		mask_ip=self.cul_mask(mask)
		dst_ip=self.IpAdd(dst_ip,-1)


		if debug =="false":
			os.system("sudo docker exec %s route add -net %s netmask %s gw %s"%(router_id,dst_ip,mask_ip,forward_ip))
		cmd="sudo docker exec %s route add -net %s netmask %s gw %s"%(router_id,dst_ip,mask_ip,forward_ip)

		self.logger.log_save(cmd,self.caseins,"info")
		#print "sudo docker exec %s route add -net %s netmask %s gw %s"%(router_id,dst_ip,mask_ip,forward_ip)


	#Host ip分配
	def HostIpDistribution(self,link_list,network_core_list,conf,user_id):
		start_ip=conf["host"]["start_ip"]
		host_data_list=[]
		router_data_list=[]
		for count in xrange(len(network_core_list)) :
			network_core_list[count]["link_router_ip"]={}
			network_core=network_core_list[count]
			bridge_id="br_"+network_core["id"]

			#作为路由器的docker，id
			router_id_docker=user_id+"_router_"+str(count+1)

			#网络核心处保存生成的网关ip
			network_core["switch_id"]=bridge_id
			network_core["as_gateway_ip"]=self.IpAdd(start_ip,1)


			#为路由器添加连接主机的ip，默认eth0
			self.IpConfigRouter(router_id_docker,network_core["as_gateway_ip"],bridge_id,"eth0",24)

			save_data={
			        "real_id": router_id_docker,
			        "router_id": network_core["id"],
			        "host_num": network_core["host_num"],
			        "image": network_core["image"],
			        "vncport": 0
			}
			router_data_list.append(save_data)


			host_ip=self.IpAdd(start_ip,2)

			for count_host in xrange(len(network_core["host_type"])):

				host_dict=network_core["host_type"][count_host]
				docker_id_pre=user_id+"_"+network_core["id"]+"_"+str(count_host)+"_"
				network_core["host_type"][count_host]["docker_id_pre"]=docker_id_pre
				gateway_ip=network_core["as_gateway_ip"]

				if host_dict["type"]=="docker":
					host_ip,docker_list=self.IpConfigDocker(host_dict,docker_id_pre,host_ip,host_dict["host_num"],network_core["id"],gateway_ip)
					host_data_list.extend(docker_list)
				#此处kvm分配ip
				else :
					kvm_conf_file_path=conf["host"]["compose_file_path"]+"user/"+user_id+"/setip.bat"
					host_ip,kvm_list=self.KvmNetConfig(host_dict,docker_id_pre,host_ip,host_dict["host_num"],gateway_ip,kvm_conf_file_path)
					host_data_list.extend(kvm_list)
			start_ip=self.IpAdd(start_ip,256)

		return network_core_list,host_data_list,router_data_list

	#配置kvm网络
	def KvmNetConfig(self,host_dict,kvm_id_pre,ip,num,gateway_ip,path):
		kvm_data_list=[]
		for count in xrange(num):
			#print "配置kvm！"
			kvm_id =kvm_id_pre+str(count+1)
			self.EditKvmNetFile(ip,gateway_ip,path)
			cmd1="sudo virt-copy-in -d %s %s /"%(kvm_id,path)
			cmd2='virsh start %s'%kvm_id
			if debug =="false":				
				os.system(cmd1)				
				os.system(cmd2)
			self.logger.log_save(cmd1,self.caseins,"info")
			self.logger.log_save(cmd2,self.caseins,"info")
			#print "sudo virt-copy-in -d %s %s /"%(kvm_id,path)
			#print 'virsh start %s'%kvm_id			
			save_data={
				"real_id": kvm_id,
				"router_id":host_dict["router_id"] ,
				"cluster_id":host_dict["id"],
				"image": host_dict["image"],
				"type": "kvm",
				"config": {
					"cpu_num": host_dict["config"]["cpu_num"],
					"mem": host_dict["config"]["mem"]
					},
				"bridge": host_dict["bridge"],
				"vncport": host_dict["vnc_port_start"]+count,
				"ip":ip
			}
			kvm_data_list.append(save_data)
			ip=self.IpAdd(ip,1)

		return ip,kvm_data_list

		



	#编辑kvm网络配置脚本
	def EditKvmNetFile(self,ip,gateway,path):
		file_object = open(path, 'a')
		str_conf="@echo off\r\n"
		file_object.write(str_conf)
		str_conf='netsh interface ip set address "bridge" static %s 255.255.255.0 %s 1'%(ip,gateway)
		file_object.write(str_conf)
		file_object.close( )






	#Router间ip分配
	def RouterIpDistribution(self,link_list,network_core_list,conf,user_id):
		router_start_ip=conf["host"]["router_start_ip"]
		for count in xrange(len(link_list)):
			link_relation=link_list[count]
			bridge_name="br_router_"+str(link_relation["link"][0])+"_"+str(link_relation["link"][1])
			eth_name="br_"+str(link_relation["link"][0])+"_"+str(link_relation["link"][1])
			link_relation["bridge_name"]=bridge_name

			router_index_0=link_relation["link"][0]
			router_index_1=link_relation["link"][1]

			#记录生成ip
			ip_link=[]

			#为一方路由器配置ip
			router_start_ip=self.IpAdd(router_start_ip,1)
			router_ip_0=router_start_ip
			router_id_docker=network_core_list[router_index_0]["docker_id"]
			self.IpConfigRouter(router_id_docker,router_start_ip,bridge_name,eth_name,30)
			ip_link.append(router_start_ip)

			#另一方路由器配置ip
			router_start_ip=self.IpAdd(router_start_ip,1)
			router_ip_1=router_start_ip
			router_id_docker=network_core_list[router_index_1]["docker_id"]
			self.IpConfigRouter(router_id_docker,router_start_ip,bridge_name,eth_name,30)
			ip_link.append(router_start_ip)


			#记录相连节点的ip，index，以便进行路由算法
			network_core_list[router_index_0]["link_router_ip"][str(router_index_1)]=\
			[network_core_list[router_index_1]["as_gateway_ip"],24,router_ip_1]

			network_core_list[router_index_1]["link_router_ip"][str(router_index_0)]=\
			[network_core_list[router_index_0]["as_gateway_ip"],24,router_ip_0]



			#产生子网掩码为30的广播网段
			router_start_ip=self.IpAdd(router_start_ip,2)

			link_list[count]["ip_list"]=ip_link

		return link_list,network_core_list


		

			
	'''
	功能：dijkstra算法
	输入：边的连接关系，起始节点，终止节点
	输出：到达终止节点的第一跳节点
	'''
	def dijkstra(self,edges, from_node, to_node):
		flag=False#标记是否找到路径
		g = defaultdict(list)
		for l,r,c in edges:
			g[l].append((c,r))
		q, seen = [(0,from_node,())], set()
		while q:
			(cost,v1,path) = heappop(q)
			(cost,v1,path)
			if v1 not in seen:
				seen.add(v1)
				path = (v1, path)
				if v1 == to_node:
					flag=True
					break
				for c, v2 in g.get(v1, ()):
					if v2 not in seen:
						heappush(q, (cost+c, v2, path))
		if not flag:
			path=()
			return 65535

		if len(path)>0:
			path_list=[]
			path_list.append(path[0])
			right = path[1]
			while len(right)>0:
				path_list.append(right[0])
				right = right[1]
		length=len(path_list)
		return path_list[length-2]


	#为docker添加路由表
	def AddRouteTable(self,link_list,network_core_list,conf,user_id):
		router_num=len(network_core_list)

		#关系矩阵矩阵生成
		edges=[]
		for link_dict in link_list:
			edges.append((link_dict["link"][0],link_dict["link"][1],1))
			edges.append((link_dict["link"][1],link_dict["link"][0],1))



		#i行表示从i节点到所有节点最近距离的下一跳
		route_step_list=[]
		for i in xrange(router_num):
			tmp=[self.dijkstra(edges,i,j) for j in xrange(router_num)]
			route_step_list.append(tmp)


		for i in xrange(router_num):
			for link_index in xrange(len(route_step_list[i])):

				#要达到目标路由的下一跳路由
				next_step=route_step_list[i][link_index]

				#指定目标路由ip，例如10.0.0.1，不需要减一，下面方法已经自动减一
				target_ip=network_core_list[link_index]["as_gateway_ip"]
				if link_index==i:
					continue
				record=network_core_list[i]["link_router_ip"][str(next_step)]

				self.RouterAdd(network_core_list[i]["docker_id"],target_ip,record[1],record[2])
				print "路由器"+str(i)+"，要到达"+str(link_index)+"，下一跳为"+str(next_step)







	#网络配置总入口函数
	def NetConfig(self,link_list,network_core_list,conf,user_id):

		#配置主机ip
		network_core_list,host_data_list,router_data_list=self.HostIpDistribution(link_list,network_core_list,conf,user_id)
		print "配置主机ip完成!"

		#配置路由ip
		link_list,network_core_list=self.RouterIpDistribution(link_list,network_core_list,conf,user_id)
		print "配置路由间ip完成!"

		#添加路由表
		self.AddRouteTable(link_list,network_core_list,conf,user_id)
		print "添加路由表完成!"

		return link_list,network_core_list,host_data_list,router_data_list


	

