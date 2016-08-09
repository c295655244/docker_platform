#encoding=utf-8
import traceback  
import tornado.web
import json
from service import *


class Index(tornado.web.RequestHandler):

	def get(self):
		self.write("success!\n")


class CreateHandler(tornado.web.RequestHandler):

	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('createjson')
		try:
			data = eval(json_str)
			result = create(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "create",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))


class DeleteHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('deletejson')
		try:
			data = eval(json_str)
			result = delete(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "delete",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))

class CmdHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('cmdjson')
		try:
			data = eval(json_str)
			result = cmd(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "cmd",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))

class MonitorHostHandler(tornado.web.RequestHandler):
	def get(self):
		#print self.request.arguments
		callback = self.get_argument('data')
		json_str = self.get_argument('data_json')
		try:
			data = eval(json_str)
			result = monitor_host(data)
			str_json=json.dumps(data)
			self.write(callback+"("+str_json+");") 
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "monitor_host",
			  "msg": str(traceback.format_exc())
			}
			str_json=json.dumps(data)
			print traceback.format_exc()
			self.write(callback+"("+str_json+");") 


	def post(self):
		json_str = self.get_argument('monitorhostjson')
		try:
			data = eval(json_str)
			result = monitor_host(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "monitor_host",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))

class MonitorTopoHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('monitortopojson')
		try:
			data = eval(json_str)
			result = monitor_topo(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "monitor_topo",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))      


class MonitorClusterHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('monitorclusterjson')
		try:
			data = eval(json_str)
			result = monitor_cluster(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "monitor_cluster",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))     


class LogDayHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('logdayjson')
		try:
			data = eval(json_str)
			result = log_day(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "log_day",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))    

class LogAllHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('logalljson')
		try:
			data = eval(json_str)
			result = log_all(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "log_all",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))    


class VncHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('vncjson')
		try:
			data = eval(json_str)
			result = vnc(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "vnc",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))    

class GetImageHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('getimagejson')
		try:
			data = eval(json_str)
			result = get_image(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "get_image",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))  