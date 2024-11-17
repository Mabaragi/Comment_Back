# app/database.py

import motor.motor_asyncio
import os
from bson.objectid import ObjectId


class MongoDB:
    def __init__(self, mongo_uri: str, database: str):
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://admin:secret@localhost:27017"
        )
        # self.db = self.client.get_database("my_project")
        self.db = self.client.get_database("my_project")
