#!/bin/bash

sudo docker-compose scale ubuntu=4

sudo ovs-vsctl add-br br-int1

sudo ovs-vsctl add-br br-int2

sudo ovs-vsctl add-br br-int3


sudo ovs-docker add-port br-int1 eth0 test2_ubuntu_1
sudo docker exec test2_ubuntu_1 ifconfig eth0 10.0.0.2/24
sudo docker exec test2_ubuntu_1 route add default gw 10.0.0.1

sudo ovs-docker add-port br-int3 eth0 test2_ubuntu_2
sudo docker exec test2_ubuntu_2 ifconfig eth0 10.0.1.2/24
sudo docker exec test2_ubuntu_2 route add default gw 10.0.1.1


sudo ovs-docker add-port br-int1 eth0 test2_ubuntu_3
sudo docker exec test2_ubuntu_3 ifconfig eth0 10.0.0.1/24

sudo ovs-docker add-port br-int2 eth1 test2_ubuntu_3
sudo docker exec test2_ubuntu_3 ifconfig eth1 20.0.0.1/24


sudo ovs-docker add-port br-int3 eth0 test2_ubuntu_4
sudo docker exec test2_ubuntu_4 ifconfig eth0 10.0.1.1/24

sudo ovs-docker add-port br-int2 eth1 test2_ubuntu_4
sudo docker exec test2_ubuntu_4 ifconfig eth1 20.0.0.2/24

sudo docker exec test2_ubuntu_4 route add -net 10.0.0.0 netmask 255.255.255.0 gw 20.0.0.1

sudo docker exec test2_ubuntu_3 route add -net 10.0.1.0 netmask 255.255.255.0 gw 20.0.0.2


