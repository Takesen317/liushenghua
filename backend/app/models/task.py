"""
Task model
"""
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON, func
from app.core.database import Base


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String(36), primary_key=True)  # tsk_ prefix
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    file_id = Column(String(36), ForeignKey("files.id"), nullable=False, index=True)

    # Status: pending, processing, completed, failed
    status = Column(String(20), nullable=False, default="pending")

    # Progress 0-100
    progress = Column(Integer, default=0)

    # Current processing step
    current_step = Column(String(50), nullable=True)

    # Style options
    style = Column(String(20), default="warm")  # warm, lively, lyrical, documentary
    voice = Column(String(20), default="xiaoxiao")  # xiaoxiao, yunyang, yunxia
    music_style = Column(String(20), default="gentle")  # gentle, cheerful, melancholy, epic

    # AI generated content
    ai_description = Column(Text, nullable=True)
    result_data = Column(JSON, nullable=True)  # {video_url, audio_url, music_url}

    # Error handling
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
