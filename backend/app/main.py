"""
留声画 - Photo Voice Narrator
FastAPI Application Entry Point
"""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, files, tasks, share


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    # Startup: create database tables
    import app.models  # noqa: F401 - import to register models
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: cleanup if needed
    pass


app = FastAPI(
    title="留声画 API",
    description="AI-powered photo narration generator",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["认证"])
app.include_router(files.router, prefix="/api/v1/files", tags=["文件"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["任务"])
app.include_router(share.router, prefix="/api/v1/share", tags=["分享"])


@app.get("/results/{task_id}/{filename}")
async def serve_video(task_id: str, filename: str):
    """Serve video files"""
    video_path = os.path.join(settings.UPLOAD_DIR, "results", task_id, filename)
    # Convert to absolute path and normalize separators
    video_path = os.path.abspath(video_path)
    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    return {"error": "Video not found"}, 404


@app.get("/")
async def root():
    return {"message": "留声画 API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
