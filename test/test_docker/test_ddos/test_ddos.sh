sudo ovs-vsctl add-br br-ddos

sudo docker-compose scale server=1 client=2

sudo ovs-docker add-port br-ddos eth0 testddos_server_1
sudo docker exec testddos_server_1 ifconfig eth0 10.0.0.1/24

sudo ovs-docker add-port br-ddos eth0 testddos_client_1
sudo docker exec testddos_client_1 ifconfig eth0 10.0.0.2/24

sudo ovs-docker add-port br-ddos eth0 testddos_client_2
sudo docker exec testddos_client_2 ifconfig eth0 10.0.0.3/24


#sudo docker exec testddos_client_1 python /ddos/attack.py http://10.0.0.1
#sudo docker exec testddos_client_2 python /ddos/attack.py http://10.0.0.1
