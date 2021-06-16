# syntax=docker/dockerfile:1
FROM python:3.7-alpine
ENV PLACE /usr/sbin/app
RUN mkdir -p "${PLACE}"
COPY . "${PLACE}"
WORKDIR "${PLACE}"
RUN pip install -r requirements.txt
EXPOSE 5000
