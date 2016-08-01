#coding=utf-8
import sys,os
import time
from functools import wraps
  
def fn_timer(function):
	@wraps(function)
	def function_timer(*args, **kwargs):
		t0 = time.time()
		result = function(*args, **kwargs)
		t1 = time.time()
		print ("Total time running %s: %s seconds" %
		    (function.func_name, str(t1-t0))
		    )
		return result
	return function_timer


@fn_timer
def create_time(num,path):
	path=path+"/docker-compose.yaml"
	compose_cmd="sudo  docker-compose -f  %s  scale  ubuntu=%s"%(path,num)
	print compose_cmd
	os.system(compose_cmd)


def del_time(path):
	path=path+"/docker-compose.yaml"
	stop_cmd="sudo  docker-compose -f  %s  stop"%(path)
	print stop_cmd
	os.system(stop_cmd)
	rm_cmd="sudo  docker-compose -f  %s  rm -f"%(path)
	print rm_cmd
	os.system(rm_cmd)


if __name__ == '__main__':
	create_time(sys.argv[1],sys.path[0])
	del_time(sys.path[0])