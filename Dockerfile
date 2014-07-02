FROM ubuntu:14.04

MAINTAINER lafolle <karan@humblepaper.com>

ENV DEBIAN_FRONTEND noninteractive

RUN apt-get update -y 
RUN apt-get install -y pandoc texlive-latex-base texlive-xetex latex-xcolor texlive-math-extra texlive-latex-extra texlive-fonts-extra curl wget git fontconfig make

# Install pip and Flask
RUN apt-get install -y python-setuptools && easy_install pip
RUN pip install Flask

EXPOSE 8800

RUN mkdir /conservice
WORKDIR /conservice
ADD . /conservice

entrypoint ["python", "main.py"]
