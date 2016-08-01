#coding:utf8
import libvirt 
import os,sys
import re
import time 

from xml.etree import ElementTree as ET 



reload(sys)
sys.setdefaultencoding('utf-8')
 



conn = libvirt.open('qemu:///system') 
dom = conn.listDomainsID() 
for i in dom: 
	vmm_id = conn.lookupByID(i) 
	vmm_name = vmm_id.name() 
	vmm_id_str = str(vmm_name) 
	vmm_xml_name = vmm_id_str + '.' + 'xml' 
	vmm_xml_path = '/tmp/' + vmm_xml_name 
	print vmm_xml_path 

	 
	vmm_xml_open = ET.parse(vmm_xml_path) 
	path_list=[] 
	path = vmm_xml_open.findall('.//source') 
	for i in path: 
		file1 = i.attrib 
		filename=file1.get('file') 
		if filename: 
			path_list.append(filename) 
	 
#    print path_list 
	interface_list = [] 
	interface = vmm_xml_open.findall('.//target') 
	for j in interface: 
		interface_network = j.attrib 
		dev1 = interface_network.get('dev') 
		dev3 = 'vnet' 
		dev2 = str(dev1) 
		if dev3 in dev2: 
			interface_list.append(dev1) 
	 
	print interface_list 
	 

 
	totalrx_byte = 0 
	totaltx_byte = 0 
	for interfaceinfo_path in interface_list: 
		print interfaceinfo_path
		interfaceinfo = vmm_id.interfaceStats(interfaceinfo_path) 
		totalrx_byte = totalrx_byte + interfaceinfo[0] 
		totaltx_byte = totaltx_byte + interfaceinfo[4] 
	print "收包 totalrx_byte:",totalrx_byte
	print "发包 totaltx_byte:",totaltx_byte

	totalcpu =   'cpu'
	totalcpu_usage = 0 
	cpu_time =  vmm_id.info()[4] 
	time1 = time.time() 
	time.sleep(0.5)
	time2 = time.time() 
	cpu_new_time = vmm_id.info()[4] 
	print vmm_id.info()
	cpu_usage=(cpu_new_time - cpu_time)/((time2 - time1)*10000000)
	totalcpu_usage = float('%0.2f'%cpu_usage)

	if totalcpu_usage>100:
		totalcpu_usage=100.0
	print "cpu使用率：",totalcpu_usage,"%"

	name="winxp"
	#根据实例名获取进程ID
	pid=(os.popen("ps aux|grep "+name+" | grep -v 'grep' | awk '{print $2}'").readlines()[0])
	memstatus=0
	#linux下 /proc/pid(进程ID）/smaps 下保存的是进程内存映像信息，比同一目录下的maps文件更详细些
	for line in file('/proc/%d/smaps' % int(pid),'r'):
		if re.findall('Private_',line):
		#统计Private内存信息量
			memstatus+=int(re.findall('(\d+)',line)[0])
	memstatus=get_memory(pid)
	memusage='%.2f' % (int(memstatus)*100.0/int(vmm_id.info()[2]))

	print memusage
		 




