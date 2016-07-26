import libvirt 

import os 
import time 
from xml.etree import ElementTree as ET 
 
 

conn = libvirt.open('qemu:///system') 


dom = conn.listDomainsID() 
for i in dom: 
    vmm_id = conn.lookupByID(i) 
    vmm_name = vmm_id.name() 
    vmm_id_str = str(vmm_name) 
    print vmm_id_str
    vmm_dom_xml = vmm_id.XMLDesc(0) 
    vmm_xml_name = vmm_id_str + '.' + 'xml' 
    vmm_xml_path = '/tmp/' + vmm_xml_name 
    print vmm_xml_path 
    if os.path.exists(vmm_xml_path): 
        pass 
    else : 
        os.mknod(vmm_xml_path) 
 
    xml_open = open(vmm_xml_path,'w') 
    for lines in vmm_dom_xml: 
        xml_open.write(lines) 
    xml_open.close() 
     
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
     
    totalrd =   'rd' 
    totalrd_byte = 0 
    totalwr =   'wr' 
    totalwr_byte = 0 
    totalrx = 'rx' 
    totalrx_byte = 0 
    totaltx =  'tx' 
    totaltx_byte = 0 
    totalrp =  'rp' 
    totalrx_packet = 0 
    totaltp =  'tp' 
    totaltx_packet = 0 
 
    for image_file in  path_list:   
        print image_file 
#        size = vmm_id.blockInfo(image_file,0) 
        block_status = vmm_id.blockStatsFlags(image_file) 
        print block_status

        totalrd_byte = totalrd_byte + block_status['rd_bytes'] 
        totalwr_byte = totalwr_byte + block_status['wr_bytes'] 
    print block_status
    print totalrd_byte    
    print totalwr_byte 
 
 
    for interfaceinfo_path in interface_list: 
        print interfaceinfo_path
        interfaceinfo = vmm_id.interfaceStats(interfaceinfo_path) 
        totalrx_byte = totalrx_byte + interfaceinfo[0] 
        totalrx_packet = totalrx_packet + interfaceinfo[1] 
        totaltx_byte = totaltx_byte + interfaceinfo[4] 
        totaltx_packet = totaltx_packet + interfaceinfo[5] 
    print "totalrx_byte:",totalrx_byte
    print "totaltx_byte:",totaltx_byte
 
    totalmem =   'actual' 
    totalmem_data = 0 
    rssmem =   'rss' 
    rssmem_data = 0 
    mem_status = vmm_id.memoryStats() 
    print "mem_status:",mem_status
    totalmem_data = mem_status['actual'] 
    rssmem_data = mem_status['rss']   
    print totalmem_data 
    print rssmem_data    
    print float(rssmem_data)/float(totalmem_data)
    totalcpu =   'cpu' 
    totalcpu_usage = 0 
    cpu_time =  vmm_id.info()[4] 
    time1 = time.time() 
    time.sleep(1) 
    time2 = time.time() 
    cpu_new_time = vmm_id.info()[4] 
    totalcpu_usage = int(((cpu_new_time - cpu_time)/((time2 - time1)*10000000))*100) 
    print totalcpu_usage 
     