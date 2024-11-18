from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
import os, dotenv
from .services.database import MongoDB
from .dependencies import mongo, get_database
from .api.endpoints.comments import router as comment_router

dotenv.load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo["mongo"] = MongoDB(
        mongo_uri=os.getenv("MONGO_LOCAL_URI"), database="fastAPI_database"
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
    collection = mongo.db.get_collection("test_collection")
    collection.insert_one({"value": "1"})
    return


app.include_router(
    router=comment_router,
    prefix="/api/comment",
    tags=["Comments"],
)
