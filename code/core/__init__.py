from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse



from os import environ,getenv
import boto3
import json
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from distutils.util import strtobool
import urllib.parse

app_name = environ.get('APP_NAME', default='')
aws_access_key_id = environ.get('ACCESS_KEY_ID', default='')
aws_secret_access_key = environ.get('SECRET_ACCESS_KEY', default='')
aws_region = environ.get('AWS_REGION', default='ap-northeast-1')
dynamo = boto3.client('dynamodb', region_name=aws_region)
s3 = boto3.client('s3', region_name=aws_region)
"""s3 = boto3.client('s3', region_name=aws_region,
                  aws_access_key_id=aws_access_key_id,
                  aws_secret_access_key=aws_secret_access_key)"""
tables = {
    "logs": environ.get('DYNAMODB_TABLE_LOGS', 'logs'),
    "prompts": environ.get('DYNAMODB_TABLE_PROMPTS', 'prompts')
}
buckets = {
    "logs": environ.get('BUCKET_LOGS', 'logs'),
    "prompts": environ.get('BUCKET_PROMPTS', 'prompts')
}
# https://docs.aws.amazon.com/lambda/latest/dg/gettingstarted-limits.html
max_response_size = 5622338


# FastAPI を初期化
app_env=getenv('APP_ENV','local')
app=FastAPI(docs_url='/docs' if app_env == 'local' else None)


def create_response(status_code: int = 200, body: dict = None, headers: dict = None):
    if body is not None:
        body = json.dumps(body, default=decimal_default_proc)
    return JSONResponse(status_code=status_code,headers=headers,content=body)


def create_event(request:Request):
    result={
        "headers": request.headers
    }
    return result



def decimal_default_proc(obj):
    if isinstance(obj, Decimal):
        return float(obj)
    raise TypeError


def split_list(list, sub):
    for i in range(0, len(list), sub):
        yield list[i:i+sub]


# UnixtimeをJSTに変換
def unix_time_to_jst(unix_time: int = None):
    if unix_time is None:
        return None
    JST = timezone(timedelta(hours=+9), 'JST')
    t = datetime.fromtimestamp(unix_time).replace(
        tzinfo=timezone.utc).astimezone(tz=JST)
    return t.strftime('%Y/%m/%d %H:%M:%S')


def extract_event(request: Request):
    if "aws_event" in request.scope:
        return request.scope["aws.event"]
    else:
        res=dict()
        #body=(request.body())
        #print(f'got body->{body}')
        res["queryStringParameters"]=dict(request.query_params)
        res["pathParameters"]=dict(request.path_params)
        return res