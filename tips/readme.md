注意：
1.所有由compose创建的docker序号由1开始，其他由0开始
2.格式化json，ctrl+alt+j
3.github push命令：
git init
git add --all
git remote rm origin
git commit -m "first commit"
git remote add origin https://github.com/c295655244/docker_platform.git
git push -u origin +master
"+"可以强行推送
之后只需

git add --all
git commit -m "first commit"
git push -u origin +master

3.解决kvm创建Unable to add port vnet0 to OVS bridge问题

sudo apt-get install apparmor-utils
sudo aa-complain /etc/apparmor.d/*

参考文献:http://www.spinics.net/linux/fedora/libvirt-users/msg04599.html


4.解决apt-get依赖问题：


http://blog.csdn.net/chenbang110/article/details/7506190
