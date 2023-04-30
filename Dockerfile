FROM python:3.8.12-slim-buster

WORKDIR /app

USER root

RUN pip install --upgrade pip
RUN pip install rasa

COPY . .

EXPOSE 8080
