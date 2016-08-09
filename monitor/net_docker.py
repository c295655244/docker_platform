#! /usr/bin/env python
#-*-coding:utf-8-*-

import sys,re
import subprocess 



class DockerNetMonitor():
	def __init__(self):
		super(Monitor, self).__init__()
		#连接本地docker demon
		#需要提前更改/etc/default/docker文件，添加：DOCKER_OPTS="-H=unix:///var/run/docker.sock -H=0.0.0.0:6732" 
		self.conn=httplib.HTTPConnection('0.0.0.0:6732')
		self.config=ReadDockConf()
		self.db=MysqlOperate(self.config)