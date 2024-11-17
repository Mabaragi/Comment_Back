# app/database.py

import motor.motor_asyncio
import os
from bson.objectid import ObjectId


class MongoDB:
    def __init__(self, client, db):
        self.client = client
        self.db = db

    @classmethod
    async def create(cls):
        # 비동기 작업 수행
        client = motor.motor_asyncio.AsyncIOMotorClient(
            "mongodb://admin:secret@localhost:27017"
        )
        db = client.test_database
        collection = db.test_collection
        document = {"key": "value"}
        result = await collection.insert_one(document)
        return

    # 컬렉션 선택
    def get_collection(self, collection_name: str):

        item_collection = self.database.get_collection(collection_name)
