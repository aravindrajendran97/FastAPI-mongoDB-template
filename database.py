import motor.motor_asyncio
import configparser
from pymongo import MongoClient

config = configparser.ConfigParser()
config.read('.env')

MONGODB_URL = config["default"]["DB_URL"]
MONGODB_NAME = config["default"]["DB_NAME"]

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client[MONGODB_NAME]

# for creating index 
# this will only work first time when you are creating collections
# can not create index after adding data to collection
pymongo_client = MongoClient(MONGODB_URL)
pymongo_db = pymongo_client[MONGODB_NAME]

collection = pymongo_db['jobs']
collection.create_index("job_id", unique=True)

collection = pymongo_db['resumes']
collection.create_index("candidate_id", unique=True)
pymongo_client.close()

