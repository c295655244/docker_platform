#coding=utf-8
from collections import defaultdict
from heapq import *


class Dijkstra(object):



	def ip2num(self,ip):
		ip=[int(x) for x in ip.split('.')]
		return ip[0] <<24 | ip[1]<<16 | ip[2]<<8 |ip[3]


	def num2ip(self,num):
		return '%s.%s.%s.%s' %( (num & 0xff000000) >>24,
			(num & 0x00ff0000) >>16,
			(num & 0x0000ff00) >>8,
			num & 0x000000ff )
	#计算掩码
	def cul_mask(self,mask_num):
		return self.num2ip(0xffffffff << (32-mask_num))

		
	#ip加num
	def IpAdd(self,ip,num):
		return self.num2ip(self.ip2num(ip)+num)



	
	# 创建关系列表
	def CreateEdge(self,List):
		return [ (link_dict["link"][0],link_dict["link"][1],1) for link_dict in List]

	#dijkstra算法,
	#输入：边的连接关系，起始节点，终止节点
	#输出：到达终止节点的第一跳节点
	def dijkstra(self,edges, from_node, to_node):
		flag=False#标记是否找到路径
		g = defaultdict(list)
		for l,r,c in edges:
			g[l].append((c,r))
		q, seen = [(0,from_node,())], set()
		while q:
			(cost,v1,path) = heappop(q)
			(cost,v1,path)
			if v1 not in seen:
				seen.add(v1)
				path = (v1, path)
				if v1 == to_node:
					flag=True
					break
				for c, v2 in g.get(v1, ()):
					if v2 not in seen:
						heappush(q, (cost+c, v2, path))
		if not flag:
			path=()
			return 65535

		if len(path)>0:
			path_list=[]
			path_list.append(path[0])
			right = path[1]
			while len(right)>0:
				path_list.append(right[0])
				right = right[1]
		length=len(path_list)
		#print path_list
		return path_list[length-2]


	def AddRouteTable(self):
		router_num=6

		#此处替换矩阵生成函数
		edges=self.data()


		#i行表示从i节点到所有节点最近距离的下一跳
		route_step_list=[]
		for i in xrange(router_num):
			tmp=[self.dijkstra(edges,i,j) for j in xrange(router_num)]
			print tmp
			route_step_list.append(tmp)


		for i in xrange(router_num):
			







	def data(self):
		### ==================== Given a list of nodes in the topology shown in Fig. 1.
		### ==================== Given constants matrix of topology.
		M=99999	# This represents a large distance. It means that there is no link.
		### M_topo is the 2-dimensional adjacent matrix used to represent a topology.
		M_topo = [
		[M,M,1,M,M,M],
		[M,M,1,M,M,M],
		[1,1,M,1,1,M],
		[M,M,1,M,M,1],
		[M,M,1,M,M,M],
		[M,M,M,1,M,M]
		]	

		### --- Read the topology, and generate all edges in the given topology.
		edges = []	
		for i in range(len(M_topo)):
			for j in range(len(M_topo[0])):
				if i!=j and M_topo[i][j]!=M:
			
					edges.append((i,j,M_topo[i][j]))### (i,j) is a link; M_topo[i][j] here is 1, the length of link (i,j).
		return 	edges	




	def test(self):
		edges=self.data()
		print "=== Dijkstra ==="
		Shortest_path = self.dijkstra(edges,0, 5)
		print 'The shortest path is ',Shortest_path

if __name__ == '__main__':
	demo=Dijkstra()
	demo.AddRouteTable()