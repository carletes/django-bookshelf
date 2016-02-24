FROM python:2.7

RUN groupadd django && useradd -m -g django -d /home/django django

RUN set -x \
    && apt-get update \
    && apt-get install -y \
         postgresql-client

COPY requirements.txt /home/django/requirements.txt

ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade -r /home/django/requirements.txt

RUN pip install --upgrade psycopg2
