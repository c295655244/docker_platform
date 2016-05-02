#!/bin/bash


sudo docker-compose stop ubuntu

sudo docker-compose rm -f

sudo ovs-vsctl del-br br-int1

sudo ovs-vsctl del-br br-int2

sudo ovs-vsctl del-br br-int3
