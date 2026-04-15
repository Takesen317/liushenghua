"""
Share model
"""
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey, func
from app.core.database import Base


class Share(Base):
    __tablename__ = "shares"

    id = Column(String(36), primary_key=True)
    task_id = Column(String(36), ForeignKey("tasks.id"), nullable=False, index=True)
    share_code = Column(String(20), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime, nullable=True)  # NULL = never expires
    view_count = Column(Integer, default=0)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
