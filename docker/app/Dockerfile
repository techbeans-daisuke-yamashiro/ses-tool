FROM python:3.11-slim
# 基本セットアップ
RUN apt update && \
  apt install -y nodejs npm awscli docker.io jq curl
#RUN apt -y install docke
COPY ./docker/app/bashrc /root/.bashrc
ENV SHELL=/bin/bash

WORKDIR /app
#FastAPIのセットアップ
COPY ./docker/app/requirements.txt /tmp
COPY ./docker/app/start.sh /usr/local/bin
RUN chmod +x /usr/local/bin/start.sh
COPY ./code/requirements.txt /tmp/requirements-app.txt
RUN pip install -r /tmp/requirements.txt && \ 
pip install -r /tmp/requirements-app.txt
#Serverless frameworkのセットアップ
RUN npm -g install serverless@v3.38 \
  serverless-attach-managed-policy \
  serverless-layers \ 
  serverless-python-requirements  \
  serverless-offline

#RUN cd /tmp && npm -g install

#awslocalのセットアップ
ARG KEY
ARG SECRET
ARG ENDPOINT
RUN aws configure set aws_access_key_id ${KEY}  && \
aws configure set aws_secret_access_key ${SECRET} && \
aws configure set endpoint-url ${ENDPOINT} && \
aws configure set output json



# アプリの設定’
ENV BUCKET_LOGS=logs-local
ENV SERVERLESS_DEPLOYMENT_BUCKET=${DEPLOYMENT_BUCKET}
ENV STAGE=${STAGE}
ENV DYNAMODB_TABLE_PROMPTS=prompts-${STAGE}
ENV DYNAMODB_TABLE_LOGS=logs-${STAGE}

#CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]
EXPOSE 3000
CMD ["/usr/local/bin/start.sh"]

