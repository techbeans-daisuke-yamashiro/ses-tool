FROM python:3.11-slim
WORKDIR /app
COPY ./docker/app/bashrc /root/.bashrc
COPY ./docker/app/requirements.txt /tmp
RUN pip install -r /tmp/requirements.txt