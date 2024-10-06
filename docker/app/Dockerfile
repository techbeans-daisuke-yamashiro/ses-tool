FROM python:3.11-slim
WORKDIR /app
COPY ./docker/app/bashrc /root/.bashrc
COPY ./docker/app/requirements.txt /tmp
RUN apt update && apt upgrade -y \
  && apt install -y curl awscli jq \
  && pip install -r /tmp/requirements.txt
