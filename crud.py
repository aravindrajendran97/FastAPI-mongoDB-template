from datetime import datetime
import schemas
from database import db
from fastapi.encoders import jsonable_encoder

import logging

logger = logging.getLogger("app.crud")


async def get_documents():
    cursor = db['<collection>'].find()
    docs = await cursor.to_list(100000) #length=100000
    return docs


async def add_documents(attribute1, attribute2):
    try:
        db_doc = schemas.Schema1(attribute1=attribute1,
                                attribute2=attribute2
                                )
        db_doc = jsonable_encoder(db_doc)
        new_doc = await db["<collection>"].insert_one(db_doc)
        created_doc = await db["<collection>"].find_one({"_id": new_doc.inserted_id})
        return created_doc

    except Exception as e:
        logger.error(f'error in adding documents {e}')
        return None

async def remove_documents(attribute1):
    try:
        delete_doc = await db["<collection>"].delete_one({"attribute1": attribute1})
        if delete_doc.deleted_count == 1:
            return True
        return False
    
    except Exception as e:
        logger.info(f"error in remove documents {e}")
        return None

