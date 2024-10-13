from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse



from os import environ,getenv
import boto3
import json
from decimal import Decimal
from datetime import datetime, timezone, timedelta
from distutils.util import strtobool
import urllib.parse

# FastAPI を初期化
app_env=getenv('APP_ENV','local')
app=FastAPI(docs_url='/docs' if app_env == 'local' else None)


#AWSクライアントを初期化

aws=boto3.Session(
    profile_name="default") if app_env == 'local' else boto3.Session() 



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


# requestからeventを展開
def extract_event(request: Request):
    if "aws_event" in request.scope:
        print(f'called via serverless')
        return request.scope["aws.event"]
    else:
        print(f'called via uvicorn')
        res=dict()
        #body=(request.body())
        #print(f'got body->{body}')
        res["queryStringParameters"]=dict(request.query_params)
        res["pathParameters"]=dict(request.path_params)
        return res