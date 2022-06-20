FROM python:latest
ENV PYTHONUNBUFFERED 1
ENV WORKDIR=/gun
RUN mkdir -p ${WORKDIR}
WORKDIR ${WORKDIR}
COPY ./requirements.txt ${WORKDIR}
RUN /bin/bash -c "pip install -r requirements.txt"
