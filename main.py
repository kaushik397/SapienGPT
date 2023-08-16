from AI21 import LLM
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from log import log
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
#data type
status = True
class Item(BaseModel):
    APIkey:str
    question:str

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    errors = []
    for error in exc.errors():
        field = '.'.join(error['loc'])
        message = error['msg']
        errors.append({'field': field, 'message': message})

    return JSONResponse(
        status_code=422,
        content={'detail': 'Validation error', 'errors': errors},
    )

@app.post("/items")
async def RequestedData(item:Item):
    # if 'name' not in item:
    #     raise RequestValidationError(errors=[{'loc': ['name'], 'msg': 'field required'}])
    item=item.dict()
    print(item)
    apikey=item['APIkey']
    question=item['question']
    log(data=f"{apikey,question}",status=status)
    response = LLM(question=question,apikey=apikey,status=status)
    if response!='':
        return response
    else:
        return {"question":"invalid"}