FROM python:3.11.4-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip

COPY ./core/requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY ./core /usr/src/app/

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

