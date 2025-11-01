from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from .auth import router as auth_router
from .posts import router as posts_router
import os

app = FastAPI(title="Echo FastAPI")

origins = [
    "http://localhost:3000",                  
    "https://echo-frontend.onrender.com"      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(posts_router)

@app.get("/")
def root():
    return {"message": "Echo backend running"}

frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend/build")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
