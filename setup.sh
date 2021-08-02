#!/bin/bash
# OS Detection + Installation of required base modules

# load /etc/os-release
source /etc/os-release

# find the OS and install
if [ $ID == "ubuntu" ]; then
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get install python3 python3-pip -y
	sudo snap install ngrok
	pip3 install meraki flask pyngrok pprintpp
elif [ $ID == "centos" ]; then
	sudo yum update
	sudo yum upgrade
	# NEED TO VERIFY THIS PART
	sudo yum install python3 python3-pip ngrok-client
	pip3 install meraki flask pyngrok pprintpp
else
	echo $ID
	echo "Cannot detect compatible OS"
fi


