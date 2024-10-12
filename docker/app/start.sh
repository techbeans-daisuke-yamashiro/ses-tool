#!/bin/bash

# serverless offlineを起動
sls offline --verbose --host 0.0.0.0 --reloadHandler &

# uvicornでアプリ起動
python handler.py