FROM python:3.6

LABEL Author="Zvi Baratz" Name=pylabber Version=0.0.1

EXPOSE 8000

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements/common.txt
