"""
留声画 - Photo Voice Narrator
FastAPI Application Entry Point
"""
import os
import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse

from app.core.config import settings
from app.core.database import engine, Base
from app.api.v1 import auth, files, tasks, share

# Configure logging
logging.basicConfig(
    level=logging.INFO if settings.DEBUG else logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    logger.info("Starting 留声画 API...")
    # Startup: create database tables
    import app.models  # noqa: F401 - import to register models
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")
    yield
    # Shutdown: cleanup if needed
    logger.info("Shutting down 留声画 API...")


app = FastAPI(
    title="留声画 API",
    description="AI-powered photo narration generator",
    version="1.0.0",
    lifespan=lifespan
)

# Security headers middleware
@app.middleware("http")
async def security_headers(request: Request, call_next):
    """Add security headers"""
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    return response


@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Add unique request ID for tracing"""
    request_id = str(uuid.uuid4())[:8]
    request.state.request_id = request_id

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


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
    # Validate task_id and filename contain no path traversal
    if ".." in task_id or "/" in task_id or "\\" in task_id:
        raise HTTPException(status_code=400, detail="Invalid task ID")
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(status_code=400, detail="Invalid filename")

    # Validate file extension
    allowed_exts = {".mp4", ".webm", ".mov"}
    ext = os.path.splitext(filename)[-1].lower()
    if ext not in allowed_exts:
        raise HTTPException(status_code=400, detail="Invalid file type")

    # Ensure path is within expected directory
    base_dir = os.path.abspath(os.path.join(settings.UPLOAD_DIR, "results"))
    video_path = os.path.abspath(os.path.join(base_dir, task_id, filename))

    if not video_path.startswith(base_dir):
        raise HTTPException(status_code=403, detail="Access denied")

    if os.path.exists(video_path):
        return FileResponse(video_path, media_type="video/mp4")
    raise HTTPException(status_code=404, detail="Video not found")


@app.get("/")
async def root():
    return {"message": "留声画 API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
