import motor.motor_asyncio
import configparser

config = configparser.ConfigParser()
config.read('.env')

MONGODB_URL = config["default"]["DB_URL"]

client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
db = client.recommenders