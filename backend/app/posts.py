from fastapi import APIRouter, HTTPException, Depends, Header
from .database import db
from .models import PostCreate, CommentCreate
from .utils import verify_token
from bson import ObjectId
from datetime import datetime

router = APIRouter(prefix="/posts", tags=["posts"])

def to_json(doc):
    doc = dict(doc)
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc

@router.get("/")
async def list_posts(user: dict = Depends(verify_token)):
    cursor = db.posts.find().sort("created_at", -1)
    posts = []
    async for p in cursor:
        posts.append(to_json(p))
    return posts

@router.post("/")
async def create_post(post: PostCreate, user: dict = Depends(verify_token)):
    data = post.dict()
    data.update({"likes": 0, "comments": [], "liked_by": [], "created_at": datetime.utcnow()})
    result = await db.posts.insert_one(data)
    return {"post_id": str(result.inserted_id)}

@router.post("/{post_id}/like")
async def like_post(post_id: str, user = Depends(verify_token)):
    username =  user["username"]
    try:
        oid = ObjectId(post_id)
    except:
        raise HTTPException(400, "Invalid post id")
    post = await db.posts.find_one({"_id": oid})
    if not post:
        raise HTTPException(404, "Post not found")
    if username in post.get("liked_by", []):
        return {"message": "Already liked", "likes": post["likes"]}
    await db.posts.update_one(
        {"_id": oid},
        {"$inc": {"likes": 1}, "$push": {"liked_by": username}}
    )
    updated = await db.posts.find_one({"_id": oid})
    return {"message": "Liked", "likes": updated.get("likes", 0)}


@router.post("/{post_id}/comment")
async def add_comment(post_id: str, comment: CommentCreate, user: dict = Depends(verify_token)):
    username = user["username"]
    try:
        oid = ObjectId(post_id)
    except:
        raise HTTPException(400, "Invalid post id")
    post = await db.posts.find_one({"_id": oid})
    if not post:
        raise HTTPException(404, "Post not found")
    comment_doc = comment.dict()
    comment_doc.update({"post_id": post_id, "created_at": datetime.utcnow()})
    result = await db.comments.insert_one(comment_doc)
    await db.posts.update_one({"_id": oid}, {"$push": {"comments": str(result.inserted_id)}})
    return {"comment_id": str(result.inserted_id)}

@router.get("/{post_id}/comments")
async def get_comments(post_id: str, user: dict = Depends(verify_token)):
    comments = []
    cursor = db.comments.find({"post_id": post_id}).sort("created_at", -1)
    async for c in cursor:
        c = dict(c)
        c["_id"] = str(c["_id"])
        comments.append(c)
    return comments
