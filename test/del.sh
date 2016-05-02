#!/bin/bash


sudo ovs-docker del-ports br-int1  test_ubuntu_1
sudo ovs-docker del-ports br-int2  test_ubuntu_2
sudo ovs-docker del-ports br-int1  test_ubuntu_3
sudo ovs-docker del-ports br-int2  test_ubuntu_3

sudo docker-compose stop ubuntu

sudo docker-compose rm -f

sudo sudo ovs-vsctl del-br br-int1

sudo sudo ovs-vsctl del-br br-int2
