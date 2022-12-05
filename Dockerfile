FROM python:3.8

RUN apt-get update && apt-get install -y net-tools postgresql-client

RUN mkdir -p /home/app/
COPY . /home/app/

WORKDIR /home/app/backend/
RUN pip3 install -r requirements.txt


