FROM python:3.6 AS builder

LABEL Author="Zvi Baratz"
LABEL Name=pylabber
LABEL Version=0.0.1

WORKDIR /app

COPY . .
COPY pylabber/.env /app/pylabber/

EXPOSE 8000

RUN pip install -r requirements.txt

CMD python manage.py makemigrations && \
    python manage.py migrate && \
    python manage.py runserver
