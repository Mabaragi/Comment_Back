from fastapi import FastAPI
import os, dotenv
from .services import database

dotenv.load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": f"World {os.getenv("MONGO_LOCAL_URI")}"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/database")
async def test_database():
    result = await database.MongoDB.create()
    return result