#!/bin/bash

virsh destroy test1

virsh undefine test1

echo "正在删除test1镜像"
#rm -f /var/lib/libvirt/images/test1


virsh destroy test2

virsh undefine test2

echo "正在删除test1镜像"
#rm -f /var/lib/libvirt/images/test2


sudo ovs-vsctl del-br br-kvm
