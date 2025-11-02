from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str

class PostCreate(BaseModel):
    title: str
    content: str
    username: str

class PostOut(BaseModel):
    id: str = Field(..., alias="_id")
    title: str
    content: str
    username: str
    likes: int
    comments: List[str] = []
    created_at: datetime

class CommentCreate(BaseModel):
    username: str
    text: str

class CommentOut(BaseModel):
    id: str = Field(..., alias="_id")
    post_id: str
    username: str
    text: str
    created_at: datetime
