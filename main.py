from AI21 import LLM
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
from log import log
#data type
status = True
class Item(BaseModel):
    APIkey:str
    question:str

app = FastAPI()
@app.get("/api/v1/")
def read_root():
    return {"200": "OK"}

@app.post("/api/v1/items/")
async def RequestedData(item:Item):
    apikey=item.APIkey
    question=item.question
    log(data=f"{apikey,question}",status=status)
    return LLM(question=question,apikey=apikey,status=status)
