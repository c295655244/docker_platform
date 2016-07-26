##!/usr/bin/env python
#coding:utf8

'''
功能：
利用virsh命令行，根据create_file(json)创建并运行kvm下winxp的虚拟机
'''

import json,os,sys
import xml.etree.ElementTree as ET

'''
注意进行修改
'''
create_file="create2.json"
basic_img="winxpwxw"


class QiuckCreateKvm():
    vm_nodes =[]

    def __init__(self):
        self.LoadInfor()

    def LoadInfor(self):
        vm_file = open(create_file)
        vm_str = vm_file.read()
        self.vm_nodes = dict(eval(vm_str))
        #eval:将JSON的字符串解析成JSON数据格式
        #再整体转为字典格式

    def EidtXml(self,node):
        #获取xml文件的根节点
        tree = ET.parse(node['xml'])
        domain = tree.getroot()
        #修改新虚拟机的域名称
        name = domain.find('./name')
        name.text = node['domain']
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
        nat_interface = devices.find("./interface[@type='bridge']")
        nat_mac = nat_interface.find('mac')
        nat_mac.set('address', node['nat_mac'])

        
        tree.write(node['xml'])
        print ("true2")
        return img

    def CreateKvms(self):
        node = {}
        
        length=len(self.vm_nodes['data']['network_topo']['network_core_list'])
        for i in range(0,length): 
            content_json=self.vm_nodes['data']['network_topo']['network_core_list'][i]['host_type'][0]['type']
            #找到了kvm格式的字段
            if content_json=="kvm":
                #将文件中的虚拟机信息存入节点
                total_num=int(self.vm_nodes['data']['network_topo']['network_core_list'][i]['host_num'])
                for j in range(1,total_num+1):
                    
                    #获得domain
                    user_id=self.vm_nodes['data']['user_info']['user_id']
                    router_id=self.vm_nodes['data']['network_topo']['network_core_list'][i]['id']
                    node['domain'] = str(user_id)+'_'+str(router_id)+'_'+str(i)+'_'+str(j)
                    print ("domain is:")
                    print node['domain']
                    
                    #获得操作系统类型
                    node['os'] = self.vm_nodes['data']['network_topo']['network_core_list'][i]['host_type'][0]['image']
                    print ("os is:")
                    print node['os']
                    
                    #获得vncport
                    node['vncport'] = int(self.vm_nodes['data']['network_topo']['network_core_list'][i]['start_vncport'])+j-1
                    print("vncport is:")
                    print node['vncport']

                    #获得mac地址
                    node['nat_mac'] = self.vm_nodes['data']['network_topo']['network_core_list'][i]['start_mac']+str(j-1)
                    print ("mac is:")
                    print node['nat_mac']

                    #获得memory大小
                    mem=str(self.vm_nodes['data']['network_topo']['network_core_list'][i]['host_type'][0]['config']['mem'])
                    node['memory']=int(mem[:-1])*1024
                    print ("memory is:")
                    print  node['memory']

                    #获得cpu的个数
                    cpu_num=self.vm_nodes['data']['network_topo']['network_core_list'][i]['host_type'][0]['config']['cpu_num']
                    node['cpu_num']=cpu_num
                    print ("cpu number is:")
                    print node['cpu_num']

                    #获得xml文件名
                    node['xml'] = '%s.xml'%node['domain']
                    print ("xml file is:")
                    print node['xml']

                    #获得镜像路径
                    node['diskimg'] = '/var/lib/libvirt/images/%s'%node['domain']
                    print ("route is:")
                    print node['diskimg']
 
                    #通过原始镜像配置得到新虚拟机的xml文件
                    os.system('virsh dumpxml %s > %s'%(basic_img, node['xml']))
                    #修改新虚拟机的xml文件，并获取原始镜像的位置信息
                    img = self.EidtXml(node)

                    print u'正在创建虚拟机：%s'%node['domain']
                    os.system('cp %s %s'%(img, node['diskimg']))
                    
                    #从xml定义新虚拟机的域
                    os.system('virsh define %s.xml'%node['domain'])
                    os.system('rm %s'%node['xml'])       
                    os.system('virsh start %s'%node['domain'])

                    print u'虚拟机%s创建成功！'%node['domain']
                    print '------------------------------------------------------------------------'
                    print '------------------------------------------------------------------------'
   

if __name__ == '__main__':
    try:
        Kvm = QiuckCreateKvm()
        Kvm.CreateKvms()
    except:
        print ("wrong")




