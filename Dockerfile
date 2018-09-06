FROM python:3.5-jessie

ENV PYTHONUNBUFFERED 1

ENV WORKDIR=/gun
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}

COPY ./gun.py ${WORKDIR}
COPY ./requirements.txt ${WORKDIR}
COPY ./settings.py ${WORKDIR}
COPY ./.cache-* ${WORKDIR}

RUN /bin/bash -c "pip install -r requirements.txt"
