"""
Celery Tasks for async AI processing
"""
import os
from pathlib import Path
from datetime import datetime, timezone

# Try to initialize Celery
_celery_app = None
_celery_available = False

try:
    from celery import Celery
    from app.core.config import settings

    _celery_app = Celery("liushenghua")
    _celery_app.config_from_object({
        'broker_url': settings.REDIS_URL,
        'result_backend': settings.REDIS_URL,
        'task_serializer': 'json',
        'accept_content': ['json'],
        'result_serializer': 'json',
        'timezone': 'Asia/Shanghai',
        'enable_utc': True,
    })
    _celery_available = True
    print("Celery initialized successfully")
except (ImportError, OSError) as e:
    print(f"Warning: Celery not available: {e}")
    print("Tasks will be processed synchronously in development mode.")


def _to_relative_path(path: str) -> str:
    """Convert absolute path to relative path (relative to results/)"""
    if not path:
        return ""
    # Normalize backslashes to forward slashes
    path = path.replace('\\', '/')
    # Extract just the part after "results/"
    if "results" in path:
        return path.split("results")[-1].lstrip("/\\")
    # If no "results" in path, assume it's already a relative path like "tsk_xxx/file.mp4"
    # Return as-is
    return path


def process_narration_task(task_id: str):
    """
    Process a narration request (can be called async or sync)
    """
    from app.core.database import SessionLocal
    from app.models.task import Task
    from app.models.file import File
    from app.services import process_narration

    db = SessionLocal()

    try:
        # Get task from database
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return {"error": "Task not found"}

        # Check if task was cancelled before we start processing
        # For sync processing, status might be "pending" (not yet set to "processing")
        if task.status == "failed":
            return {"status": task.status, "message": "Task was cancelled"}

        # Update status to processing
        task.status = "processing"
        task.current_step = "正在加载文件"
        task.progress = 5
        task.updated_at = datetime.now(timezone.utc)
        db.commit()

        # Get file info
        file_record = db.query(File).filter(File.id == task.file_id).first()
        if not file_record:
            raise Exception("File not found")

        # Step 1: Analyze image
        task.current_step = "正在分析图像"
        task.progress = 20
        task.updated_at = datetime.now(timezone.utc)
        db.commit()

        # Step 2: Generate narration text
        task.current_step = "正在生成解说词"
        task.progress = 40
        task.updated_at = datetime.now(timezone.utc)
        db.commit()

        # Step 3: Synthesize voice
        task.current_step = "正在合成语音"
        task.progress = 55
        task.updated_at = datetime.now(timezone.utc)
        db.commit()

        # Step 4: Generate music
        task.current_step = "正在生成背景音乐"
        task.progress = 70
        task.updated_at = datetime.now(timezone.utc)
        db.commit()

        # Step 5: Compose video
        task.current_step = "正在合成视频"
        task.progress = 85
        task.updated_at = datetime.now(timezone.utc)
        db.commit()

        # Check if task was cancelled before running AI pipeline
        db.refresh(task)
        if task.status == "failed":
            return {"status": task.status, "message": "Task was cancelled"}

        # Run the complete AI pipeline
        from app.core.config import settings
        output_dir = Path(settings.UPLOAD_DIR) / "results" / task_id
        output_dir.mkdir(parents=True, exist_ok=True)

        result = process_narration(
            image_path=file_record.file_path,
            style=task.style,
            voice=task.voice,
            music_style=task.music_style,
            output_dir=str(output_dir)
        )

        # Check if task was cancelled after AI pipeline completed
        db.refresh(task)
        if task.status == "failed":
            return {"status": task.status, "message": "Task was cancelled"}

        # Update task with results - store relative paths for cross-platform compatibility
        task.status = "completed"
        task.progress = 100
        task.current_step = "已完成"
        task.ai_description = result.get("ai_description", "")
        task.result_data = {
            "video_url": _to_relative_path(result.get("video_path", "")),
            "audio_url": _to_relative_path(result.get("audio_path", "")),
            "music_url": _to_relative_path(result.get("music_path", "")),
        }
        task.updated_at = datetime.now(timezone.utc)
        db.commit()

        return {
            "task_id": task_id,
            "status": "completed",
            "ai_description": result.get("ai_description", ""),
            "video_path": result.get("video_path", "")
        }

    except Exception as e:
        # Update task as failed
        try:
            task = db.query(Task).filter(Task.id == task_id).first()
            if task:
                task.status = "failed"
                task.error_message = str(e)
                task.progress = 0
                task.updated_at = datetime.now(timezone.utc)
                db.commit()
        except Exception as inner_e:
            print(f"Failed to update task {task_id} status: {inner_e}")

        return {"error": str(e), "task_id": task_id}

    finally:
        db.close()


# Register with Celery if available
if _celery_app:
    @_celery_app.task(name="process_narration_task")
    def celery_process_narration_task(task_id: str):
        return process_narration_task(task_id)


def queue_task(task_id: str):
    """Queue a task for async processing (idempotent - same task_id won't be queued twice)"""
    if _celery_app and _celery_available:
        try:
            # Use task_id as Celery task_id for deduplication
            # Celery ignores duplicates if task is already pending/processing
            _celery_app.send_task(
                "process_narration_task",
                args=[task_id],
                task_id=task_id  # Idempotency key
            )
            return True
        except Exception as e:
            print(f"Failed to queue task: {e}")
    return False


def cleanup_old_files():
    """Periodic task to clean up old uploaded files"""
    # TODO: Implement cleanup logic
    pass


def get_celery_app():
    """Get the Celery app instance for task control operations"""
    return _celery_app
