from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import os, dotenv
from .services.database import MongoDB
from .dependencies import mongo, get_database
from .api.endpoints.crawl import router as crawl_router
from .api.endpoints.user import router as user_router
import json

dotenv.load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo["mongo"] = MongoDB(
        mongo_uri=os.getenv("MONGO_LOCAL_URI"),
    )
    yield
    mongo["mongo"].client.close()


app = FastAPI(lifespan=lifespan)


@app.get("/")
def read_root():
    return {"Hello": f"World {os.getenv("MONGO_LOCAL_URI")}"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}


@app.get("/database")
async def test_database(mongo: MongoDB = Depends(get_database)):
    database = mongo.db
    collection = database.get_collection("comments")
    # print(collection)
    comments_cussor = collection.find()
    comments = await comments_cussor.to_list()
    return {"response": comments}


app.include_router(
    router=crawl_router,
    prefix="/api/crawl",
    tags=["Crawling"],
)
app.include_router(
    router=user_router,
    prefix="/api/user",
    tags=["User"],
)
