#!/bin/bash

sudo docker-compose scale ubuntu=3

sudo ovs-vsctl add-br br-int1

sudo ovs-vsctl add-br br-int2


sudo ovs-docker add-port br-int1 eth0 test_ubuntu_1
sudo docker exec test_ubuntu_1 ifconfig eth0 10.0.0.2/24
sudo docker exec test_ubuntu_1 route add default gw 10.0.0.1

sudo ovs-docker add-port br-int2 eth0 test_ubuntu_2
sudo docker exec test_ubuntu_2 ifconfig eth0 10.0.1.2/24
sudo docker exec test_ubuntu_2 route add default gw 10.0.1.1


sudo ovs-docker add-port br-int1 eth0 test_ubuntu_3
sudo docker exec test_ubuntu_3 ifconfig eth0 10.0.0.1/24

sudo ovs-docker add-port br-int2 eth1 test_ubuntu_3
sudo docker exec test_ubuntu_3 ifconfig eth1 10.0.1.1/24

#sudo docker exec test_ubuntu_3 route add -net 10.0.0.0 netmask 255.255.255.0 dev eth0

#sudo docker exec test_ubuntu_3 route add -net 10.0.1.0 netmask 255.255.255.0 dev eth1


