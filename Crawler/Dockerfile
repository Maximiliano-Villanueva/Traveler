FROM python:3.8
ENV PYTHONUNBUFFERED 1

WORKDIR /home

RUN mkdir -p Traveler
RUN mkdir -p shared-files

#RUN apk add --no-cache mariadb-connector-c-dev
#RUN apk update && apk add python3 python3-dev mariadb-dev build-base && pip3 install mysqlclient && apk del python3-dev mariadb-dev build-base

#RUN apk add netcat-openbsd

ADD ./Traveler Traveler

RUN pip install --upgrade pip && pip install -r Traveler/requirements.txt
EXPOSE 8080
