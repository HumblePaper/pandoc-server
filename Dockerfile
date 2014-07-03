FROM ubuntu:14.04

MAINTAINER lafolle <karan@humblepaper.com>

ENV DEBIAN_FRONTEND noninteractive

ENV http_proxy http://10.200.1.26:8080
ENV https_proxy https://10.200.1.26:8080


#RUN apt-get update -y 
RUN apt-get install -y pandoc 

# Install pip and Flask
RUN apt-get install -y python-setuptools && easy_install pip
RUN pip install Flask

EXPOSE 8800

RUN mkdir /conservice
WORKDIR /conservice
VOLUME . /conservice

entrypoint ["python", "main.py"]
