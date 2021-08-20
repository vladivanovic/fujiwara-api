#!/bin/bash

# Kickstart PostGreSQL for WSL2 or OS where it doesn't autostart
if ps ax |grep -v grep | grep 'postgres' > /dev/null
  then
    echo 'PostGreSQL is running'
  else
    sudo /etc/init.d/postgresql start
fi

# Kickstart Main Flask App in Docker
docker-compose start main_app
