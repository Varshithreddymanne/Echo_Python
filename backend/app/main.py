from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app import auth, posts  

app = FastAPI(title="Echo App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api")
app.include_router(posts.router, prefix="/api")

frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend/build")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")
    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        """
        Serve React frontend for all non-API routes.
        Prevents React build from intercepting /api routes.
        """
        if full_path.startswith("api"):
            raise HTTPException(status_code=404, detail="API route not found")

        index_path = os.path.join(frontend_path, "index.html")
        if os.path.exists(index_path):
            return FileResponse(index_path)
        return {"message": "index.html not found"}
