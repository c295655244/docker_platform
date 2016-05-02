#coding=utf-8
import sys,os
import json
import traceback
import ConfigParser



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


def ReadTopoData():
    files=os.path.dirname(sys.path[0])+"/data/data.json"
    with open(files, "r") as f:
        try:
            data= json.load(f)
        except Exception, e:
            print "读取json失败！"
    return data
    
def WriteTopoData(json_data):
    files=os.path.dirname(sys.path[0])+"/data/result.json"
    try:
        json.dump(json_data, open(files, 'w'))
    except Exception, e:
        print "读取json失败！"


if __name__ == '__main__':
    print ReadTopoData()
    ReadDockConf()