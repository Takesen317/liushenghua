"""
File model
"""
from sqlalchemy import Column, String, BigInteger, DateTime, ForeignKey, func
from app.core.database import Base


class File(Base):
    __tablename__ = "files"

    id = Column(String(36), primary_key=True)  # fil_ prefix
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_type = Column(String(20), nullable=False)  # jpg, png, webp
    file_size = Column(BigInteger, nullable=False)
    description = Column(String(500), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
