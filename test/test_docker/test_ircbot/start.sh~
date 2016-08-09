#data:2016.8.8
#author:niyuandong@wis-eye.com
#title:autorun for the ircbot1.4.1

#sleep 30s to wait for the kvm server
sleep 20s

#testing the ircserver
count=0
max=1000000
while test $count -lt $max
do
	if ping -w 1 -c 1 10.0.5.2 | grep "1 packets received" >/dev/null
	then
		let "count = $max"
	else
		let "count = $count + 1"
	fi
done

#when ircserver is up ,sleep 10s for the unrealircd service
sleep 5s

#start the bot client
/BotClient 10.0.5.2

sleep 365d
