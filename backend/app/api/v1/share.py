"""
Share management API routes
"""
import uuid
import random
import string
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.task import Task
from app.models.share import Share

router = APIRouter()


def generate_share_code(length: int = 8) -> str:
    """Generate random share code"""
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


class ShareCreate(BaseModel):
    task_id: str
    expires_days: Optional[int] = None


@router.post("")
async def create_share_link(
    share_data: ShareCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a share link for a completed task"""
    task_id = share_data.task_id
    expires_days = share_data.expires_days

    # Verify task exists and belongs to user
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=404,
            detail="任务不存在"
        )

    if task.status != "completed":
        raise HTTPException(
            status_code=400,
            detail="只能分享已完成的任务"
        )

    # Check if share already exists
    existing = db.query(Share).filter(Share.task_id == task_id).first()
    if existing:
        return {
            "share_code": existing.share_code,
            "url": f"/share/{existing.share_code}",
            "expires_at": existing.expires_at.isoformat() if existing.expires_at else None
        }

    # Create new share
    expires_at = None
    if expires_days:
        from datetime import timedelta
        expires_at = datetime.utcnow() + timedelta(days=expires_days)

    share_code = generate_share_code()

    # Ensure unique share code
    while db.query(Share).filter(Share.share_code == share_code).first():
        share_code = generate_share_code()

    share = Share(
        id=f"shr_{uuid.uuid4().hex[:12]}",
        task_id=task_id,
        share_code=share_code,
        expires_at=expires_at
    )
    db.add(share)
    db.commit()

    return {
        "share_code": share_code,
        "url": f"/share/{share_code}",
        "expires_at": expires_at.isoformat() if expires_at else None
    }


@router.get("/{share_code}")
async def get_shared_content(
    share_code: str,
    db: Session = Depends(get_db)
):
    """Get shared content by share code (public endpoint)"""
    share = db.query(Share).filter(Share.share_code == share_code).first()

    if not share:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="分享不存在"
        )

    # Check expiration
    if share.expires_at and share.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=status.HTTP_410_GONE,
            detail="分享链接已过期"
        )

    # Get task with result
    task = db.query(Task).filter(Task.id == share.task_id).first()
    if not task or task.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="内容不可用"
        )

    # Increment view count
    share.view_count += 1
    db.commit()

    # Get file info
    from app.models.file import File
    file = db.query(File).filter(File.id == task.file_id).first()

    return {
        "ai_description": task.ai_description,
        "result_data": task.result_data,
        "filename": file.filename if file else "未知",
        "view_count": share.view_count
    }
