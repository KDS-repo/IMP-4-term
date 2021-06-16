# syntax=docker/dockerfile:1
FROM python:3.7-alpine
#ENV PLACE /usr/sbin/app
#RUN mkdir -p "${PLACE}"
#COPY . "${PLACE}"
#WORKDIR "${PLACE}"
#ADD requirements.txt "${PLACE}"
#RUN pip install -r requirements.txt
#ADD . "${PLACE}"
#EXPOSE 5000


ENV PYTHONUNBUFFERED 1
RUN mkdir /usr/sbin/app
WORKDIR /usr/sbin/app
ADD requirements.txt /usr/sbin/app/
RUN pip install -r requirements.txt
ADD . /usr/sbin/app/
EXPOSE 5000
