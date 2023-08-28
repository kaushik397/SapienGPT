from AI21 import LLM
from typing import Union
from fastapi import FastAPI,File, UploadFile
from pydantic import BaseModel, ValidationError, root_validator
from log import log
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
import os
#data type
status = False
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
#basic health check
@app.get("/",status_code=200)
def status():
    return{"status":200}
# below is audio file related code

@app.get("/get_audio/")
async def get_audio():
    file_path = os.path.join("temp", "output.mp3")  # Replace with the actual file path
    return FileResponse(file_path, headers={"Content-Disposition": "attachment; filename=output.mp3"})

#items
@app.post("/items")
async def RequestedData(item:Item):
    item=item.dict()
    print(item)
    apikey=item['APIkey']
    question=item['question']
    log(data=f"{apikey,question}",status=status)
    response = LLM(question=question,apikey=apikey,status=True)
    if response!='':
        return {"response":response}
    else:
        return {"question":"invalid"}