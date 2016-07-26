#coding=utf-8
import sys,os
import socket
import json


class ApiOperate(object):
	def __init__(self):
		address = ('192.168.202.130', 1111)
		self.sock_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # s = socket.socket()
		self.sock_conn.bind(address)
		self.sock_conn.listen(5)

	def receive(self):
		self.client_conn, self.addr = self.sock_conn.accept()
		print self.addr,"连接！"
		data=self.client_conn.recv(65535)
		#print json.loads(data)
		print data
		self.client_conn.send("ok!\n")
		self.client_conn.close()
		self.sock_conn.close()


if __name__ == '__main__':
	demo=ApiOperate()
	demo.receive()


		



