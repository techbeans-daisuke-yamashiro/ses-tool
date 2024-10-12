from core import app
from mangum import Mangum
from core import extract_event
from fastapi import Request,Response,APIRouter
from fastapi.responses import JSONResponse
import uvicorn
import json

router=APIRouter()

@app.get("/hello")
def hello(request:Request):
    return JSONResponse(content={"message": "updated" },
                        status_code=200)

@app.post("/echo")
def event(request: Request):
    try:
        event=request.scope["aws.event"]
        print(f'called via serverless')
    except KeyError as e:
         print(f'called via unicorn')
         event=extract_event(request)
    print(f'event->{event}')
    return JSONResponse(content={"event": event},
                        status_code=200)

@router.get("/redirect")
def redirect():
    headers = {"Location": "https://yahoo.co.jp"}
    return Response(status_code=302,headers=headers)

handler=Mangum(app)

if __name__ == "__main__":
    uvicorn.run(app="handler:app",host="0.0.0.0",port=3003,reload=True)
