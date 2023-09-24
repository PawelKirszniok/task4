ARG PYTHON_VERSION=3.9.13
ARG PYTHON_BUILD_VERSION=$PYTHON_VERSION-buster

FROM python:${PYTHON_BUILD_VERSION}


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN python -m pip install --upgrade pip
COPY ./requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /task4

COPY ./task4 .

EXPOSE 8000
