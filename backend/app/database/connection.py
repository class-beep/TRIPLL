from pymongo import MongoClient
import motor.motor_asyncio
from app.config import settings

# Synchronous PyMongo client for seed scripts and sync operations
client = MongoClient(settings.MONGODB_URI)
db = client[settings.DATABASE_NAME]

# Async Motor client for FastAPI routes
async_client = motor.motor_asyncio.AsyncIOMotorClient(settings.MONGODB_URI)
async_db = async_client[settings.DATABASE_NAME]

def get_db():
    return db

def get_async_db():
    return async_db
