FROM python:3.7.1-alpine3.8

RUN apk add --no-cache build-base libxml2-dev libxslt-dev

COPY requirements/requirements.txt /app/
WORKDIR /app

RUN pip install pip-tools
RUN pip-sync

COPY . /app/
RUN pip install -e .

ENV PYTHONUNBUFFERED 1

CMD python -ic 'import fmi'
