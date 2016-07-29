#encoding=utf-8

import tornado.web
import json
from service import create,delete,cmd,moniter_host,moniter_topo

class CreateHandler(tornado.web.RequestHandler):

    def get(self):
    	self.write("success!")

    def post(self):
	json_str = self.get_argument('createjson')
	data = eval(json_str)
	result = create(data)
	self.write(json.dumps(result))

class DeleteHandler(tornado.web.RequestHandler):
	def post(self):
		json_str = self.get_argument('deletejson')
		deletejson = eval(json_str)

		#测试数据，在使用时删除
		deletejson = {
		    "host_id":
			"21asd56wad1",
		    "operate":"moniter"
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

class MoniterHostHandler(tornado.web.RequestHandler):
	def post(self):
		json_str = self.get_argument('moniterhostjson')
		moniterhostjson = eval(json_str)

		#测试数据，使用时删除
		moniterhostjson = {
		  "host_id": [
		    "21asd56wad1",
		    "21asd56fasf"
		  ],
		  "operate": "moniter_host"
		}

		result = moniter_host(moniterhostjson)
		self.write(json.dumps(result))

class MoniterTopoHandler(tornado.web.RequestHandler):
	def post(self):
		json_str = self.get_argument('monitertopojson')
		monitertopojson = eval(json_str)

		#测试数据，使用时删除
		monitertopojson = {
		  "topo_id":"21asd56wad1",
		  "operate": "moniter_topo"
		}

		result = moniter_topo(monitertopojson)
		self.write(json.dumps(result))		