#coding=utf-8
import sys,os
import json
import traceback
import ConfigParser


#读取配置文件
def ReadDockConf():
    files=os.path.dirname(sys.path[0])+"/conf/configure.conf"
    data_conf=ConfigParser.ConfigParser()
    data_conf.read(files)
    data_dict={}
    for section in data_conf.sections():
        section_dict={}
        for item in data_conf.options(section):
            section_dict[item]=data_conf.get(section,item)
        data_dict[section]=section_dict
    return data_dict


#获取数据
def ReadTopoData(data_types):
    
    files=os.path.dirname(sys.path[0])+"/data/"+data_types+".json"
    with open(files, "r") as f:
        try:
            data= json.load(f)
        except Exception, e:
            print "读取json失败！"
            raise e
    return data
    
def WriteTopoData(json_data,data_types):
    files=os.path.dirname(sys.path[0])+"/data/"+data_types+"_result.json"
    try:
        json.dump(json_data, open(files, 'w'))
    except Exception, e:
        print "保存json失败！"
        print traceback.format_exc()


if __name__ == '__main__':
    print ReadTopoData()
    ReadDockConf()