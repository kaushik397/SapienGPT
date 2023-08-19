from AI21 import LLM
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, ValidationError, root_validator
from log import log
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
#data type
status = True
class Item(BaseModel):
    APIkey:str
    question:str
    @root_validator (pre=True,skip_on_failure=True)
    def change_input_data(cls, v):
        if len(v) < 2:
            raise ValueError("Both the fields are required")
        return v
        
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
# @ValidationError(pre=True)
# def validate_options(cls, v, values):
#     if len(v) < 2:
#         raise ValueError("At least 2 options are required")
#     return v
@app.get("/",status_code=200)
def status():
    return{"status":200}


@app.post("/items")
async def RequestedData(item:Item):
    item=item.dict()
    print(item)
    apikey=item['APIkey']
    question=item['question']
    log(data=f"{apikey,question}",status=status)
    response = LLM(question=question,apikey=apikey,status=status)
    if response!='':
        return {"response":response}
    else:
        return {"question":"invalid"}