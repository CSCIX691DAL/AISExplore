from RealTimeAIS.settings import DATABASE_NAME,PORT_NUMBER
from pymongo import MongoClient

def get_database():
    return getattr(MongoClient(port=PORT_NUMBER),DATABASE_NAME)