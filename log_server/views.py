#encoding=utf-8
import traceback  
import tornado.web
import json,os


class Index(tornado.web.RequestHandler):

	def get(self):
		self.write("success!\n")


class GetFile(tornado.web.RequestHandler):

	def get(self,date,filename):
		self.set_header ('Content-Type', 'application/octet-stream')
		self.set_header ('Content-Disposition', 'attachment; filename=' + filename)
		buf_size = 4096
		with open("./"+date+"/"+filename, 'rb') as f:
			while True:
				data = f.read(buf_size)
				if not data:
					break
				self.write(data)
		self.finish()
