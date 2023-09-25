FROM python:3.11.4-slim-bullseye

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y install netcat gcc tzdata \
  && apt-get clean

ENV TZ Africa/Nairobi
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# install python dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
COPY ./requirements-dev.txt .
RUN pip install -r requirements-dev.txt

# add app
COPY . .

EXPOSE 3100