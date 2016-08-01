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
		self.write("success!")

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

class LogMonthHandler(tornado.web.RequestHandler):
	def get(self):
		self.write("success!")

	def post(self):
		json_str = self.get_argument('logmonthjson')
		try:
			data = eval(json_str)
			result = log_month(data)
			self.write(json.dumps(result))
		except Exception, e:
			data={
			  "status": "error",
			  "data": [],
			  "operate": "log_month",
			  "msg": str(traceback.format_exc())
			}
			print traceback.format_exc()
			self.write(json.dumps(data))    