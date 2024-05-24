FROM python:3.11.4-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE = 1
ENV PYTHONNUNBUFFERED = 1

RUN pip install --upgrade pip 

COPY  ./requirements.txt /usr/src/app/requirements.txt

RUN pip3 install -r requirements.txt




COPY . /usr/src/app/


RUN python manage.py collectstatic --noinput
RUN python manage.py migrate