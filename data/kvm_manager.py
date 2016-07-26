##!/usr/bin/env python
#coding:utf8

#author hittang	<hitgwt@163.com>

import threading,time,sys,signal,os,string
import zmq, Queue, json
import xml.etree.ElementTree as ET
from dbcontrol import mongodb as mongo
import uuid

from Get_snap import cp_images
''' manager vncport alloc and recover'''
count = 1
class VncManager():

	port_queue = Queue.Queue()
	for port in range(5925, 5960):
		port_queue.put(port)

	@classmethod	
	def alloc_vncport(cls):
		assert(cls.port_queue.empty() == False)
		return cls.port_queue.get()
	@classmethod
	def recover_vncport(cls, port):
		cls.port_queue.put(port)

class Vm_Manager():
	#task_dict store all tasks
	"""docstring for Vm_Manager"""

	def __init__(self, arg):
		super(Vm_Manager, self).__init__()

	@staticmethod
	def create_vm(vm_node):
		vm_node['vncport'] = VncManager.alloc_vncport()
		vm_node['xml'] = '%s.xml'%vm_node['domain']
		vm_node['diskimg'] = '/var/lib/libvirt/images/%s'%vm_node['domain']
		os.system('virsh dumpxml %s > %s'%(vm_node['os'], vm_node['xml']))
		img = Vm_Manager.edit_kvm_xml(vm_node)
		os.system('cp %s %s'%(img, vm_node['diskimg']))
		os.system('virsh define %s.xml'%vm_node['domain'])
		os.system('rm %s'%vm_node['xml'])		
		os.system('virsh start %s'%vm_node['domain'])
		print "vm_node:",vm_node


		# vm_node['vncport'] = VncManager.alloc_vncport()
		# vm_node['xml'] = '/var/lib/libvirt/images/%s.xml'%vm_node['domain']
		# domain = vm_node['domain']
		# cp_images().scp_snap(str(vm_node['os']))
		# print vm_node['os'],999999999999999999
		# print 'domain:',domain,"\n",
		# vm_node['diskimg'] = '/var/lib/libvirt/images/%s'%vm_node['domain']
		# # os.system('virsh dumpxml %s > %s'%(vm_node['os'], vm_node['xml']))
		# os.system('cp /var/lib/libvirt/images/%s.xml %s'%(vm_node['os'], vm_node['xml']))
		# print 0000000000000000000000000000000000
		# img = Vm_Manager.edit_kvm_xml(vm_node,idd)
		# os.system('cp %s %s'%(img, vm_node['diskimg']))
		# print 1111111111111111111111111111111111
		# os.system('virsh define /var/lib/libvirt/images/%s.xml'%vm_node['domain'])
		# print 2222222222222222222222222222222222
		# # os.system('rm %s'%vm_node['xml'])
		# print 3333333333333333333333333333333333
		# os.system('virsh start %s'%vm_node['domain'])
		# print 4444444444444444444444444444444444



	@staticmethod
	def delete_vm(vm_node):
		os.system('virsh destroy %s'%vm_node['domain'])
		os.system('virsh undefine %s'%vm_node['domain'])
		os.system('rm %s'%vm_node['diskimg'])
		VncManager.recover_vncport(vm_node['vncport'])

	@staticmethod
	def edit_kvm_xml(vm_node):

		tree = ET.parse(vm_node['xml'])
		domain = tree.getroot()
		#change name
		name = domain.find('./name')
		name.text = vm_node['domain']
		#delete uuid
		uuid = domain.find('./uuid')
		domain.remove(uuid)
		#modify disk file
		devices = domain.find('./devices')

		disk = devices.find("./disk[@device='disk']")
		source = disk.find('source')
		img = source.get('file')

		#设置镜像路径
		source.set('file',vm_node['diskimg'])

		vnc = devices.find("./graphics[@type='vnc']")

		#设置vnc端口
		vnc.set('port', str(vm_node['vncport']))

		nat_interface = devices.find("./interface[@type='network']")
		nat_mac = nat_interface.find('mac')

		#设置mac地址
		nat_mac.set('address', vm_node['nat_mac'])

		#对于windows，直接使用networkinfo第0个元素的mac地址
		if (vm_node['os'] == 'winxp') or (vm_node['os'] == 'horse'):
			bridge_interface = devices.find("./interface[@type='bridge']")
			bridge_mac = bridge_interface.find('mac')
			bridge_mac.set('address', vm_node['networkinfo'][0][4])

		elif (vm_node['os'] == 'linux') or (vm_node['os'] == 'router') or (vm_node['os'] == 'ddos'):
			slot = string.atoi(nat_interface.find('address').get('slot'), 16)
			for network in vm_node['networkinfo']:
				slot += 1
				interface_e = ET.SubElement(devices,'interface')

				interface_e.set('type', 'bridge')
				mac_e = ET.SubElement(interface_e, 'mac')
				mac_e.set('address', network[4])

				source_e = ET.SubElement(interface_e, 'source')
				source_e.set('bridge', 'br0')

				model_e = ET.SubElement(interface_e, 'model')
				model_e.set('type', 'virtio')

				address_e = ET.SubElement(interface_e, 'address')
				address_e.set('bus', '0x00')
				address_e.set('domain', '0x0000')
				address_e.set('function', '0x0')
				address_e.set('slot', '0x%02x'%slot)
				address_e.set('type', 'pci')

		tree.write(vm_node['xml'])
		return img

'''store vm configinfo key: nat_mac, values: iplist macaddr route_table,software etc.'''
'''global varibale'''
class Task_Manager():
	task_dict = dict()

'''main thread: process cmd sent by kvmserver, manager all task'''
class Receive_Server_Thread(threading.Thread):

	def __init__(self, local_ip, server_port, inner_port):
		threading.Thread.__init__(self)
		'''global zmq Context'''
		zmqcontext = zmq.Context()
		self.receiver = zmqcontext.socket(zmq.REP)
		self.receiver.bind('tcp://*:%s'%server_port)
		self.inproc = zmqcontext.socket(zmq.REQ)
		self.inproc.connect('tcp://172.29.152.242:%s'%inner_port) 
		self.poller = zmq.Poller()
		self.poller.register(self.receiver, zmq.POLLIN)
		self.poller.register(self.inproc, zmq.POLLIN)
		self.local_ip = local_ip
	def run(self):
		while True:
			socks = dict(self.poller.poll())
			if self.inproc in socks and socks[self.inproc] == zmq.POLLIN:
				recv_message = json.loads(self.inproc.recv())
				self.process_inproc_status(recv_message)
			elif self.receiver in socks and socks[self.receiver] == zmq.POLLIN:
				recv_message = json.loads(self.receiver.recv())
				repy_message = self.process_message(recv_message)
				self.receiver.send(json.dumps(repy_message))

	def process_inproc_status(self, message):
		repy_message = {'type': 'repy', 'content': 'i receive the message and process it'}
		return repy_message

	def process_message(self, task):
		if task['cmdtype'] == 'create':
			return self.process_create_cmd(task)
		elif task['cmdtype'] == 'delete':
			return self.process_delete_cmd(task['taskid'])     	
		repy_message = {'type': 'repy', 'content': 'i receive the message and process it'}
		return repy_message

	def process_create_cmd(self,task):
		taskid = task['taskid']
		Task_Manager.task_dict[taskid] = task
		for vm_node in task['task']:
			Vm_Manager.create_vm(vm_node)
			vm_node['vnclink'] = '%s:%s'%(self.local_ip, vm_node['vncport'] - 5900)
			vm_node['taskid'] = taskid
			vm_node['ftpaddr'] = '172.26.253.46'
			mongo.update_node_soft(vm_node)
			print vm_node['software']
			condict = {'taskid':taskid,'nat_mac':vm_node['nat_mac']}
			mongo.op_update_taskinfo(condict,{'vnclink':vm_node['vnclink']})
		#insert db
		# self.db.insert_vm_info(task['task'])

		self.inproc.send(json.dumps(task))
		repy_message = {'type': 'repy', 'content': 'i receive the message and process it'}
		return repy_message
		
	def process_delete_cmd(self,taskid):
		try:
			task = Task_Manager.task_dict.pop(taskid)
			for vm_node in task['task']:
				Vm_Manager.delete_vm(vm_node)
		except Exception, e:
			raise e
		repy_message = {'type': 'repy', 'content': 'i receive the message and process it'}
		return repy_message

def signal_handle(signal, frame):
	print 'exit for ctrl-c'
	sys.exit()

if __name__ == '__main__':   

	signal.signal(signal.SIGINT, signal_handle)
	db = 'db'
	# heartport = '7990'
	# config_port = '7991'
	inner_port = '7992'
	local_ip = '192.168.1.108'
	server_port = '7993'
	# receive_vm_thread = Receive_Vm_Thread(heartport,db)
	# config_vm_thread = Config_Vm_Thread(config_port,inner_port,db)
	receive_server_thread = Receive_Server_Thread(local_ip,server_port,inner_port)
	receive_server_thread.setDaemon(True)
	receive_server_thread.start()
	# config_vm_thread.start()
	# receive_vm_thread.start()
	while True:
		time.sleep(999999)
