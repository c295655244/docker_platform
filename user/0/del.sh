#!/bin/bash



sudo docker-compose stop

sudo docker-compose rm -f

sudo ovs-vsctl del-br br_router_0_1
sudo ovs-vsctl del-br br_router_2_1
sudo ovs-vsctl del-br br_router_0_2
sudo ovs-vsctl del-br br_s56d2art
sudo ovs-vsctl del-br br_a56d2ayu
sudo ovs-vsctl del-br br_c56d2aio
