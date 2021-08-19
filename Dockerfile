FROM python:3.8-slim-buster

WORKDIR /app

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install python3 python3-pip python3-dev build-essential libpq-dev -y
RUN pip3 install meraki flask pyngrok psycopg2

COPY . .
