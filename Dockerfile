FROM python:3.8-slim-buster

WORKDIR ${PWD}/app

RUN apt-get update && apt-get upgrade -y && apt-get install python3 python3-pip python3-dev build-essential libpq-dev -y
RUN pip3 install meraki flask pyngrok psycopg2 docker

COPY . .
