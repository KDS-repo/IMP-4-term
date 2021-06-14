FROM python:3-alpine

ENV PLACE /usr/sbin/app

RUN mkdir -p "${PLACE}"

COPY ./Lab_1.py "${PLACE}"

WORKDIR "${PLACE}"

CMD ["python3", "Lab_1.py"]
