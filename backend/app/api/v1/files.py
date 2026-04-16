"""
File management API routes
"""
import os
import uuid
import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.file import File as FileModel
from app.schemas.file import FileResponse, FileUploadResponse

router = APIRouter()


def generate_file_id() -> str:
    """Generate file ID with fil_ prefix"""
    return f"fil_{uuid.uuid4().hex[:12]}"


def ensure_upload_dir() -> Path:
    """Ensure upload directory exists"""
    upload_path = Path(settings.UPLOAD_DIR)
    upload_path.mkdir(parents=True, exist_ok=True)
    return upload_path


@router.post("/upload", response_model=FileUploadResponse)
async def upload_file(
    file: UploadFile = File(...),
    description: str = "",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a photo file"""
    # Validate file type
    allowed_types = ["jpg", "jpeg", "png", "webp"]
    file_ext = file.filename.split(".")[-1].lower() if "." in file.filename else ""

    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型，仅支持: {', '.join(allowed_types)}"
        )

    # Read file contents
    contents = await file.read()
    file_size = len(contents)

    # Validate magic bytes to ensure content matches extension
    magic_bytes = {
        "jpg": b"\xFF\xD8\xFF",
        "jpeg": b"\xFF\xD8\xFF",
        "png": b"\x89PNG\r\n\x1a\n",
        "webp": b"RIFF",
    }
    expected_magic = magic_bytes.get(file_ext, b"")
    if file_ext == "webp":
        # WebP is RIFF....WEBP
        if not contents.startswith(b"RIFF") or b"WEBP" not in contents[:12]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="文件内容与扩展名不匹配"
            )
    elif not contents.startswith(expected_magic):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="文件内容与扩展名不匹配"
        )

    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"文件大小超过限制，最大 {settings.MAX_FILE_SIZE // (1024*1024)}MB"
        )

    # Generate file ID and path
    file_id = generate_file_id()
    upload_dir = ensure_upload_dir()
    # Sanitize filename to prevent path traversal
    safe_filename = "".join(c for c in file.filename if c.isalnum() or c in "._-")
    file_path = upload_dir / f"{file_id}_{safe_filename}"

    # Save file synchronously (more reliable)
    with open(file_path, 'wb') as f:
        f.write(contents)

    # Create database record
    db_file = FileModel(
        id=file_id,
        user_id=current_user.id,
        filename=file.filename,
        file_path=str(file_path),
        file_type=file_ext,
        file_size=file_size,
        description=description
    )
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    return FileUploadResponse(
        file_id=db_file.id,
        filename=db_file.filename,
        size=db_file.file_size,
        url=f"/api/v1/files/{db_file.id}"
    )


@router.get("/{file_id}", response_model=FileResponse)
async def get_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get file info"""
    db_file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.user_id == current_user.id
    ).first()

    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    return FileResponse(
        id=db_file.id,
        user_id=db_file.user_id,
        filename=db_file.filename,
        file_type=db_file.file_type,
        file_size=db_file.file_size,
        description=db_file.description,
        created_at=db_file.created_at.isoformat(),
        url=f"/api/v1/files/{db_file.id}"
    )


@router.delete("/{file_id}")
async def delete_file(
    file_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a file"""
    db_file = db.query(FileModel).filter(
        FileModel.id == file_id,
        FileModel.user_id == current_user.id
    ).first()

    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    # Delete physical file
    file_path = Path(db_file.file_path)
    if file_path.exists():
        file_path.unlink()

    # Delete database record
    db.delete(db_file)
    db.commit()

    return {"message": "文件已删除"}
