FROM python:3.10.4-buster

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app

WORKDIR /app
COPY ./app /app

RUN adduser --disabled-password user
USER user

