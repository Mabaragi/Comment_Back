from fastapi import APIRouter, Depends, HTTPException
from app.schemas.users import *
from app.services.database import MongoDB
from ...dependencies import get_database
from typing import Optional
from pprint import pprint
from pymongo.errors import BulkWriteError
from ...utils import hash_password, verify_password

router = APIRouter()


@router.post("/signup/")
async def signup(singup_request: SignupReqeust, mongo: MongoDB = Depends(get_database)):
    email = singup_request.email
    name = singup_request.name
    password = singup_request.password
    hashed_password = hash_password(password)
    collection = mongo.db.get_collection("users")
    existing_user = await collection.find_one({"email": email})
    if existing_user:
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    user = {"email": email, "name": name, "password": hashed_password}
    await collection.insert_one(user)

    return {"message": "회원가입 성공!"}


@router.post("/login/")
async def login(login_request: LoginRequest, mongo: MongoDB = Depends(get_database)):
    email = login_request.email
    password = login_request.password
    users = mongo.db.get_collection("users")
    user = await users.find_one({"email": email})
    if not user:
        raise HTTPException(status_code=400, detail="회원가입 되지 않은 이메일입니다.")
    if not verify_password(password, user["password"]):
        raise HTTPException(status_code=400, detail="비밀번호가 일치하지 않습니다.")
