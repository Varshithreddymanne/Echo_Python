from fastapi import FastAPI, Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os
from .auth import router as auth_router
from .posts import router as post_router

app = FastAPI(title= "Echo App")

app.include_router(auth_router)
app.include_router(post_router)

# Serve React build
frontend_path = os.path.join(os.path.dirname(__file__), "../../frontend/build")

if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=os.path.join(frontend_path, "static")), name="static")

    @app.get("/{full_path:path}")
    async def serve_react(full_path: str):
        """
        Serve React frontend for all non-API routes.
        """
        index_path = os.path.join(frontend_path, "index.html")
        return FileResponse(index_path)
