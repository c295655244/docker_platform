#coding:utf8
import sys,os
import random
from read_data import *
from set_log import *
import xml.etree.ElementTree as ET
debug=ReadDockConf()["host"]["debug"]


reload(sys)
sys.setdefaultencoding('utf-8')

class KvmOperate():

	def __init__(self):
		self.logger=Logger()
		self.caseins="demo"
		pass

	def randomMAC(self):
		mac = [ 0x52, 0x54, 0x00,
				random.randint(0x00, 0x7f),
				random.randint(0x00, 0xff),
				random.randint(0x00, 0xff) ]
		return ':'.join(map(lambda x: "%02x" % x, mac))

	def EidtXml(self,node):
		#获取xml文件的根节点
		tree = ET.parse(node['xml'])
		domain = tree.getroot()
		#修改新虚拟机的域名称
		name = domain.find('./name')
		name.text = node['id']
		#删除uuid
		uuid = domain.find('./uuid')
		domain.remove(uuid)
		#修改memeory
		memory =domain.find('./memory')
		memory.text=str(node['memory'])
		#修改cpu个数
		cpu_num=domain.find('./vcpu')
		cpu_num.text=str(node['cpu_num'])
		#修改硬件信息
		devices = domain.find('./devices')
		disk = devices.find("./disk[@device='disk']")
		source = disk.find('source')
		img = source.get('file')
		source.set('file',node['diskimg'])
		#修改VNC端口号
		vnc = devices.find("./graphics[@type='vnc']")
		vnc.set('port', str(node['vncport']))
		#修改MAC地址
		nat_interface = devices.find("./interface")
		nat_interface.set('type',"bridge")
		nat_mac = nat_interface.find('mac')
		nat_mac.set('address', node['nat_mac'])

		nat_bridge=nat_interface.find('source')
		nat_bridge.set('bridge', node['bridge'])

		# address_del=nat_interface.find('address')
		# nat_interface.remove(address_del)

		nat_interface.append(ET.fromstring("<virtualport type='openvswitch'/>"))

		tree.write(node['xml'])
		return img


	def KvmPreStart(self,host_data,argv):
		node={}

		#获得domain
		node['id'] =argv['id']

		node['bridge']=argv["bridge"]

		#获得操作系统类型
		node['os'] = host_data['image']

		#获得vncport
		node['vncport'] = argv["vnc_port"]

		#获得mac地址
		node['nat_mac'] = self.randomMAC()

		#获得memory大小
		mem=str(host_data['config']['mem'])
		node['memory']=int(mem[:-1])*1024

		#获得cpu的个数
		node['cpu_num']=host_data['config']['cpu_num']

		#获得xml文件名
		node['xml'] = argv["config"]+"user/"+str(argv["user_id"])+'/%s.xml'%node['id']

		#获得镜像路径
		node['diskimg'] = '/var/lib/libvirt/images/%s'%node['id']

		#通过原始镜像配置得到新虚拟机的xml文件
		cmd='virsh dumpxml %s > %s'%(argv['image'], node['xml'])
		os.system(cmd)
		self.logger.log_save(cmd,self.caseins,"info")
		#print cmd

		#修改新虚拟机的xml文件，并获取原始镜像的位置信息
		img = self.EidtXml(node)

		cmd='cp %s %s'%(img, node['diskimg'])
		if debug =="false":
			if not os.path.exists(node['diskimg']):
				os.system(cmd)
		self.logger.log_save(cmd,self.caseins,"info")
		#print cmd

		cmd='virsh define %s'%node['xml']
		if debug =="false":                    
			#从xml定义新虚拟机的域
			os.system(cmd)
		self.logger.log_save(cmd,self.caseins,"info")	
		#print cmd


		# cmd='virsh start %s'%node['id']
		# if debug =="false":                         
		#     os.system(cmd)
		# print cmd

		print u'虚拟机%s创建成功！'%node['id']      

		return node


	def KvmCreate(self,config,network_core_list,user_id):
		vm_nodes=network_core_list
		host_save_list={}
		vnc_port=int(config["host"]["vnc_start_port"])
		for i in xrange(len(vm_nodes)): 
			router_id=vm_nodes[i]["id"]
			router_docker_id=str(user_id)+"_"+"router"+"_"+str(i+1)
			bridge="br_"+vm_nodes[i]["id"]

			#找到了kvm格式的字段
			for j in xrange(len(vm_nodes[i]['host_type'])):

				host_data=vm_nodes[i]['host_type'][j]
				host_data["host_info"]=[]
				if host_data["type"]=="kvm":    
					host_data["router_id"]=router_id
					host_data["vnc_port_start"]=vnc_port
					host_data["bridge"]="br_"+router_id
					for count in xrange(host_data["host_num"]):
						argv={}
						argv["user_id"]=user_id
						argv["router_id"]=router_id
						argv["vnc_port"]=vnc_port
						argv["config"]=config["host"]["compose_file_path"]
						argv["image"]=host_data["image"]
						argv["bridge"]="br_"+router_id
						argv['id'] = str(user_id)+'_'+router_id+'_'+str(i)+'_'+str(count+1)
						host_info=self.KvmPreStart(host_data,argv)
						vnc_port+=1
						
		config["host"]["vnc_start_port"]=str(vnc_port)
		return  config,network_core_list




	def KvmDel(self,data_list):

		for host in data_list:  
			if host["type"]=="kvm":
				host_id=host["real_id"]
				#获得镜像路径
				diskimg= '/var/lib/libvirt/images/%s'%host_id
				
				cmd='virsh destroy %s'%host_id

				if debug =="false":                    
					os.system(cmd)
				self.logger.log_save(cmd,self.caseins,"info")
				#print cmd

				cmd='virsh undefine %s'%host_id
				if debug =="false":                    
					os.system(cmd)
				self.logger.log_save(cmd,self.caseins,"info")
				#print cmd

				cmd='rm -f %s'%diskimg
				if debug =="false":        
					pass
					#为加快运行速度，此处不再删除镜像           
					#os.system(cmd)
				self.logger.log_save(cmd,self.caseins,"info")
				#print cmd




if __name__ == '__main__':
	demo=KvmOperate()
	data=ReadTopoData("create")
	conf=ReadDockConf()

	demo.KvmCreate(conf,data["data"]["network_topo"]["network_core_list"],
		data["data"]["user_info"]["user_id"])   
   
