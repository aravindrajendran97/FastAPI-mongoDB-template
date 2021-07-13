from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, status
from typing import List
from pydantic import BaseModel
from starlette.responses import JSONResponse
from logging.handlers import RotatingFileHandler
import logging
import os
import crud

## logging settings
logger = logging.getLogger("app")
formatter = logging.Formatter('Time - %(asctime)s Module - %(name)s Level - %(levelname)s Message - %(message)s')
logger.setLevel(logging.INFO)
path="logs/resume-recommenders.log"
if not os.path.exists('logs'): os.makedirs('logs')
handler = RotatingFileHandler(path, maxBytes=1048576,backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)


app = FastAPI()


# models for request data validation
class Model1(BaseModel):
    attribute1: str

class Model2(BaseModel):
    attribute1: List[Model1]

class Model3(BaseModel):
    attribute1: str
    attribute2: list
    attribute3: datetime


# If you have default messages
status_content = {
    "success": {"status": "success"},
    "failure": {"status": "failed"},
    "not found": {"status": "not found"}
}

# GET Health check
@app.get("/")
def health():
    return {"health": "good"}

# GET request
@app.get("/docs")
async def get_docs():
    try:
        docs = await crud.get_documents()
        if docs != None:
            logger.info(f'Success in getting all documents {docs}')
            return JSONResponse(status_code=status.HTTP_200_OK, content={"result": docs})
        else:
            logger.info(f'No docs in the DB')
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=status_content['failure'])
    except Exception as e:
        logger.error(f'failed in sending all docs {e}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=status_content['failure'])

# DELETE request
@app.delete("/docs/{doc_id}")
async def remove_docs(doc_id: Model3):
    response = await crud.remove_documents(doc_id)
    if response == True:
        logger.info(f'Success in removing {doc_id} {response}')
        return JSONResponse(status_code=status.HTTP_200_OK, content=status_content['success'])
    elif response == False:
        logger.info(f'{doc_id} not found to remove resume {response}')
        return JSONResponse(status_code=status.HTTP_200_OK, content=status_content['not found'])
    else:
        logger.info(f'failed in removing {doc_id}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=status_content['failure'])

# POST request
@app.post("/docs")
async def add_docs(doc: Model3):
    response = await crud.add_documents(doc)
    if response:
        logger.info(f'Success in adding {doc}')
        return JSONResponse(status_code=status.HTTP_200_OK, content=response)
    else:
        logger.info(f'failed in adding {doc}')
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=status_content['failure'])
