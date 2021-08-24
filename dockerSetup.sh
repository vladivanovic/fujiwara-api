#!/bin/bash
# OS Detection + Installation of required base modules

# load /etc/os-release
source /etc/os-release

# find the OS and install
if [ $ID == "ubuntu" ]; then
	sudo apt-get update
	sudo apt-get upgrade
	# Previous pre-Docker installation requirements - leaving them here just in case
	#	sudo apt-get install python3 python3-pip python3-dev build-essential tmux postgresql postgresql-contrib libpq-dev -y
	# sudo snap install ngrok
	# pip3 install meraki flask pyngrok psycopg2
	# Ubuntu 20.04 Postgres initial setup, cluster start is in there for WSL2 primarily, seems to autostart on native Ubuntu
	sudo su postgres << EOF
	pg_ctlcluster 12 main start
	createdb merakihuddb;
	psql -c "CREATE USER merakihud WITH PASSWORD 'merakihudpassword';"
	psql -c "GRANT ALL PRIVILEGES ON DATABASE merakihuddb TO merakihud;"
EOF
  # Docker Installation
  sudo apt install apt-transport-https ca-certificates curl software-properties-common -y
  curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
  sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu focal stable"
  sudo apt update
  apt-cache policy docker-ce  # Confirm if Docker is using Ubuntu or Docker repo
  sudo apt install docker-ce docker-compose  # Install Docker, then Docker-Compose
  sudo systemctl status docker # Confirm if Docker service is up and enabled
  sudo usermod -aG docker ${USER}  # Add current user to run Docker without sudo
  su - ${USER}  # Become that user
  id -nG  # Test if its part of one group
  # Docker Container Build
  docker build -tag fujiwara-api .
  docker tag fujiwara-api:latest fw_mainapp:latest
  docker tag fujiwara-api:latest fw_webhook:latest
  docker tag fujiwara-api:latest fw_engineio:latest
  # Show all Docker Images
  docker images
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


