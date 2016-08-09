#encoding=utf-8

import tornado.web
import json
from service import create,delete,cmd,monitor_host,monitor_topo

class CreateHandler(tornado.web.RequestHandler):

    def get(self):
    	self.write("success!")

    def post(self):
    	json_str = self.get_argument('createjson')
    	createjson = eval(json_str)

    	#测试数据，在使用时候删除
    	createjson ={
		  "status": "success",
		  "operate": "create",
		  "caseins": "21asd56wad1",
		  "msg": "ok",
		  "data": {
		    "host_list": [
		      {
		        "router_id": "s56d2art",
		        "bridge": "br_s56d2art",
		        "real_id": "0_s56d2art_0_1",
		        "cluster_id": "asdwdadcs",
		        "vncport": 0,
		        "ip": "10.0.0.2",
		        "config": {
		          "cpu_num": "2",
		          "mem": "512m"
		        },
		        "image": "ubuntu:14.04",
		        "type": "docker"
		      },
		      {
		        "router_id": "s56d2art",
		        "bridge": "br_s56d2art",
		        "real_id": "0_s56d2art_0_2",
		        "cluster_id": "asdwdadcs",
		        "vncport": 0,
		        "ip": "10.0.0.3",
		        "config": {
		          "cpu_num": "2",
		          "mem": "512m"
		        },
		        "image": "ubuntu:14.04",
		        "type": "docker"
		      },
		      {
		        "router_id": "a56d2ayu",
		        "bridge": "br_a56d2ayu",
		        "real_id": "0_a56d2ayu_0_1",
		        "cluster_id": "asddwqda",
		        "vncport": 0,
		        "ip": "10.0.1.2",
		        "config": {
		          "cpu_num": "2",
		          "mem": "512m"
		        },
		        "image": "ubuntu:14.04",
		        "type": "docker"
		      },
		      {
		        "router_id": "a56d2ayu",
		        "bridge": "br_a56d2ayu",
		        "real_id": "0_a56d2ayu_0_2",
		        "cluster_id": "asddwqda",
		        "vncport": 0,
		        "ip": "10.0.1.3",
		        "config": {
		          "cpu_num": "2",
		          "mem": "512m"
		        },
		        "image": "ubuntu:14.04",
		        "type": "docker"
		      },
		      {
		        "router_id": "c56d2aio",
		        "bridge": "br_c56d2aio",
		        "real_id": "0_c56d2aio_0_1",
		        "cluster_id": "wegewfwe",
		        "vncport": 34567,
		        "ip": "10.0.2.2",
		        "config": {
		          "cpu_num": "2",
		          "mem": "512m"
		        },
		        "image": "winxp",
		        "type": "kvm"
		      },
		      {
		        "router_id": "c56d2aio",
		        "bridge": "br_c56d2aio",
		        "real_id": "0_c56d2aio_0_2",
		        "cluster_id": "wegewfwe",
		        "vncport": 34568,
		        "ip": "10.0.2.3",
		        "config": {
		          "cpu_num": "2",
		          "mem": "512m"
		        },
		        "image": "winxp",
		        "type": "kvm"
		      }
		    ],
		    "router_list": [
		      {
		        "router_id": "s56d2art",
		        "image": "ubuntu:14.04",
		        "real_id": "0_router_1",
		        "vncport": 0,
		        "host_num": 2
		      },
		      {
		        "router_id": "a56d2ayu",
		        "image": "ubuntu:14.04",
		        "real_id": "0_router_2",
		        "vncport": 0,
		        "host_num": 2
		      },
		      {
		        "router_id": "c56d2aio",
		        "image": "ubuntu:14.04",
		        "real_id": "0_router_3",
		        "vncport": 0,
		        "host_num": 2
		      }
		    ]
		  }
		}

    	result = create(createjson)
        self.write(json.dumps(createjson))

class DeleteHandler(tornado.web.RequestHandler):
	def post(self):
		json_str = self.get_argument('deletejson')
		deletejson = eval(json_str)

		#测试数据，在使用时删除
		deletejson = {
		    "host_id":
			"21asd56wad1",
		    "operate":"monitor"
		}

		result = delete(deletejson)
		self.write(json.dumps(result))

class CmdHandler(tornado.web.RequestHandler):
	def post(self):
		json_str = self.get_argument('cmdjson')
		cmdjson = eval(json_str)

		#测试数据，使用时删除
		cmdjson = {
		    "topo_id":"21asd56wad1",
		    "host_id":"asasd626wd",
		    "cmd":"python  demo.py",
		    "operate":"cmd"
		}


		result = cmd(cmdjson)
		self.write(json.dumps(result))

class MonitorHostHandler(tornado.web.RequestHandler):
	def post(self):
		json_str = self.get_argument('monitorhostjson')
		monitorhostjson = eval(json_str)

		#测试数据，使用时删除
		monitorhostjson = {
		  "host_id": [
		    "21asd56wad1",
		    "21asd56fasf"
		  ],
		  "operate": "monitor_host"
		}

		result = monitor_host(monitorhostjson)
		self.write(json.dumps(result))

class MonitorTopoHandler(tornado.web.RequestHandler):
	def post(self):
		json_str = self.get_argument('monitortopojson')
		monitortopojson = eval(json_str)

		#测试数据，使用时删除
		monitortopojson = {
		  "topo_id":"21asd56wad1",
		  "operate": "monitor_topo"
		}

		result = monitor_topo(monitortopojson)
		self.write(json.dumps(result))		