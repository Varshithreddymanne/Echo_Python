from fastapi import APIRouter, HTTPException, Depends, Header
from passlib.context import CryptContext
from .database import db
from .models import UserCreate, UserLogin
from .utils import create_access_token, verify_token
from typing import Optional

router = APIRouter(prefix="/auth", tags=["auth"])
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(email: str):
    return db.users.find_one({"email": email})

@router.post("/register")
async def register(user: UserCreate):
    existing = await db.users.find_one({"email": user.email})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed = pwd_ctx.hash(user.password)
    await db.users.insert_one({
        "username": user.username,
        "email": user.email,
        "password": hashed
    })
    return {"message": "User registered"}

@router.post("/login")
async def login(data: UserLogin):
    user = await db.users.find_one({"email": data.email})
    if not user or not pwd_ctx.verify(data.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"email": user["email"], "username": user["username"]})
    return {"access_token": token}
