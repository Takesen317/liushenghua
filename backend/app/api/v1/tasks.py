"""
Task management API routes
"""
import os
import uuid
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.core.config import settings
from app.models.user import User
from app.models.task import Task
from app.models.file import File
from app.schemas.task import TaskCreate, TaskResponse, TaskStatusResponse

router = APIRouter()


def generate_task_id() -> str:
    """Generate task ID with tsk_ prefix"""
    return f"tsk_{uuid.uuid4().hex[:12]}"


@router.post("", response_model=dict)
async def create_task(
    task_data: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new narration task"""
    # Verify file exists and belongs to user
    db_file = db.query(File).filter(
        File.id == task_data.file_id,
        File.user_id == current_user.id
    ).first()

    if not db_file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="文件不存在"
        )

    # Create task
    task = Task(
        id=generate_task_id(),
        user_id=current_user.id,
        file_id=task_data.file_id,
        status="pending",
        progress=0,
        style=task_data.style,
        voice=task_data.voice,
        music_style=task_data.music_style
    )
    db.add(task)
    db.commit()

    # Queue Celery task for async processing (falls back to sync if Celery unavailable)
    from app.tasks import queue_task, process_narration_task
    queued = queue_task(task.id)
    if not queued:
        print(f"Celery unavailable, processing task {task.id} synchronously...")
        # Process synchronously when Celery is not available
        process_narration_task(task.id)

    return {"task_id": task.id, "status": task.status}


@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task details"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )

    return TaskResponse(
        id=task.id,
        user_id=task.user_id,
        file_id=task.file_id,
        status=task.status,
        progress=task.progress,
        current_step=task.current_step,
        style=task.style,
        voice=task.voice,
        music_style=task.music_style,
        ai_description=task.ai_description,
        result_data=task.result_data,
        error_message=task.error_message,
        created_at=task.created_at.isoformat()
    )


@router.get("/{task_id}/status", response_model=TaskStatusResponse)
async def get_task_status(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get task processing status"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )

    return TaskStatusResponse(
        task_id=task.id,
        status=task.status,
        progress=task.progress,
        current_step=task.current_step,
        result=task.result_data
    )


@router.post("/{task_id}/cancel")
async def cancel_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cancel a running task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )

    if task.status not in ["pending", "processing"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法取消已完成或已失败的任务"
        )

    task.status = "failed"
    task.error_message = "用户主动取消"
    task.updated_at = datetime.now(timezone.utc)
    db.commit()

    # Try to revoke Celery task if running
    try:
        from app.tasks import get_celery_app
        celery_app = get_celery_app()
        if celery_app and task.status == "processing":
            celery_app.control.revoke(task_id, terminate=True)
    except Exception:
        pass  # Task may have already finished

    return {"message": "任务已取消"}


@router.post("/{task_id}/retry")
async def retry_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retry a failed task"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )

    if task.status != "failed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只能重试失败的任务"
        )

    # Reset task status
    task.status = "pending"
    task.progress = 0
    task.current_step = None
    task.error_message = None
    task.result_data = None
    task.updated_at = datetime.now(timezone.utc)
    db.commit()

    # Re-queue the task
    from app.tasks import queue_task, process_narration_task
    queued = queue_task(task.id)
    if not queued:
        print(f"Celery unavailable, processing task {task.id} synchronously...")
        process_narration_task(task.id)

    return {"task_id": task.id, "status": task.status}


@router.get("")
async def list_tasks(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    """List user's tasks"""
    # Enforce pagination limits to prevent memory issues
    max_limit = 100
    limit = min(limit, max_limit)

    tasks = db.query(Task).filter(
        Task.user_id == current_user.id
    ).order_by(Task.created_at.desc()).offset(offset).limit(limit).all()

    return {
        "tasks": [
            {
                "id": t.id,
                "file_id": t.file_id,
                "status": t.status,
                "progress": t.progress,
                "created_at": t.created_at.isoformat()
            }
            for t in tasks
        ],
        "total": db.query(Task).filter(Task.user_id == current_user.id).count()
    }


@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a task and its associated files"""
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user.id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="任务不存在"
        )

    # Delete associated files
    from app.models.file import File
    file_record = db.query(File).filter(File.id == task.file_id).first()
    if file_record and os.path.exists(file_record.file_path):
        try:
            os.remove(file_record.file_path)
        except OSError as e:
            print(f"Failed to delete file: {e}")
        db.delete(file_record)

    # Delete associated share
    from app.models.share import Share
    share_record = db.query(Share).filter(Share.task_id == task_id).first()
    if share_record:
        db.delete(share_record)

    # Delete result files directory
    results_dir = os.path.join(settings.UPLOAD_DIR, "results", task_id)
    if os.path.exists(results_dir):
        try:
            import shutil
            shutil.rmtree(results_dir)
        except OSError as e:
            print(f"Failed to delete results directory: {e}")

    # Delete task
    db.delete(task)
    db.commit()

    return {"message": "任务已删除"}
