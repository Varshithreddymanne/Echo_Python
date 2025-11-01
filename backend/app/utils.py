from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException, Header
import os
from dotenv import load_dotenv
from typing import Dict, Any

load_dotenv()

SECRET = os.getenv("JWT_SECRET", "supersecretkey")
ALGO = os.getenv("JWT_ALGORITHM", "HS256")

def create_access_token(data: dict, expires_minutes: int = 60*6):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET, algorithm=ALGO)
    return token

def verify_token(authorization: str = Header(...)) -> Dict[str, Any]: # type: ignore
    try:
        token = authorization.split(" ")[1]
        payload = jwt.decode(token, SECRET, algorithms=[ALGO])
        username = payload.get("username")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return {"username": username}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
