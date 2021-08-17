#!/bin/bash
# OS Detection + Installation of required base modules

# load /etc/os-release
source /etc/os-release

# find the OS and install
if [ $ID == "ubuntu" ]; then
	sudo apt-get update
	sudo apt-get upgrade
	sudo apt-get install python3 python3-pip python3-dev build-essential tmux postgresql postgresql-contrib libpq-dev -y
	sudo snap install ngrok
	pip3 install meraki flask pyngrok psycopg2
	# Ubuntu 20.04 Postgres initial setup, cluster start is in there for WSL2 primarily, seems to autostart on native Ubuntu
	sudo su postgres << EOF
	pg_ctlcluster 12 main start
	createdb merakihuddb;
	psql -c "CREATE USER merakihud WITH PASSWORD 'merakihudpassword';"
	psql -c "GRANT ALL PRIVILEGES ON DATABASE merakihuddb TO merakihud;"
EOF
elif [ $ID == "centos" ]; then
	sudo yum update
	sudo yum upgrade
	# NEED TO VERIFY THIS PART
	sudo yum install python3 python3-pip python3-dev build-essential ngrok-client tmux postgresql postgresql-contrib libpq-dev -y
	pip3 install meraki flask pyngrok psycopg2
	# CentOS Postgres initial setup
	sudo su postgres << EOF
	createdb merakihuddb;
	psql -c "CREATE USER merakihud WITH PASSWORD 'merakihudpassword';"
	psql -c "GRANT ALL PRIVILEGES ON DATABASE merakihuddb TO merakihud;"
EOF
else
	echo $ID
	echo "Cannot detect compatible OS"
fi


