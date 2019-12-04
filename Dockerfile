FROM python:3.6 AS builder

LABEL Author="Zvi Baratz"
LABEL Name=pylabber
LABEL Version=0.0.1

WORKDIR /app

COPY . .
COPY pylabber/docker.env /app/pylabber/.env

EXPOSE 8000

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
