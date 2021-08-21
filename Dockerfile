FROM python:3.8-slim-buster

WORKDIR ${PWD}/app

RUN apt-get update && apt-get upgrade -y && apt-get install python3 python3-pip python3-dev build-essential libpq-dev apt-transport-https ca-certificates curl gnupg2 software-properties-common -y
RUN curl -fsSL https://download.docker.com/linux/debian/gpg | apt-key add -
RUN add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/debian $(lsb_release -cs) stable"
RUN apt-get update && apt-get install docker-ce -y
RUN pip3 install meraki flask pyngrok psycopg2 docker pysnmp

COPY . .
