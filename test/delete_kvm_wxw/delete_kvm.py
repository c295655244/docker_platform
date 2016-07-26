##!/usr/bin/env python
#coding:utf8

'''
功能：
利用virsh命令行，根据create_file(json)移除kvm下winxp的虚拟机
'''

import json,os,sys
import xml.etree.ElementTree as ET

'''
注意进行修改
'''
create_file="create2.json"


class QiuckDeleteKvm():
    vm_nodes =[]

    def __init__(self):
        self.LoadInfor()

    def LoadInfor(self):
        vm_file = open(create_file)
        vm_str = vm_file.read()
        self.vm_nodes = dict(eval(vm_str))
        #eval:将JSON的字符串解析成JSON数据格式
        #再整体转为字典格式

    def DeleteKvms(self):
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
                    
                    #获得镜像路径
                    node['diskimg'] = '/var/lib/libvirt/images/%s'%node['domain']
                                
                    #删除虚拟机
                    print u'正在删除虚拟机：%s'%node['domain']
                    os.system('virsh destroy %s'%node['domain'])
                    os.system('virsh undefine %s'%node['domain'])
                    os.system('rm -f %s'%node['diskimg'])
                    print u'虚拟机%s删除成功！'%node['domain']
                    print '------------------------------------------------------------------------'
                    print '------------------------------------------------------------------------'

  
if __name__ == '__main__':
    try:
         Kvm = QiuckDeleteKvm()
         Kvm.DeleteKvms()
    except:
        print ("wrong")




