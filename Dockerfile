FROM python:3.6

LABEL Author="Zvi Baratz" Name=pylabber Version=0.0.1

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1
ENV ALLOWED_HOSTS="*" \
    DEBUG=true \
    SECRET_KEY="S0m3-$Ecr37=k33" \
    DB_HOST="db" \
    MEDIA_ROOT="/app/media" 

EXPOSE 8000

RUN mkdir /app
WORKDIR /app
COPY . /app

RUN pip install -r requirements/common.txt
