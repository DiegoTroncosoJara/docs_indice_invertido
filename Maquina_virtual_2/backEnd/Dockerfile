FROM python:3.9-alpine

ENV USER_DB = 'root'
ENV PASSWORD_DB = '123456'
ENV HOST_DB = "localhost"
ENV PORT_DB = "3306"
ENV DATA_BASE = "dbsd"

ENV DOCKER_CONTENT_TRUST=1
ENV DOCKER_REGISTRY=docker.io
ENV DOCKER_REGISTRY_MIRROR=https://registry-1.docker.io


WORKDIR /backEnd
COPY ./ /backEnd

RUN pip install -r requirements.txt
CMD ["python", "main.py"]

EXPOSE 8000