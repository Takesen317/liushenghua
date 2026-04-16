"""
File schemas
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class FileResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    filename: str
    file_type: str
    file_size: int
    description: Optional[str]
    created_at: str
    url: str  # Public download URL instead of internal path


class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    size: int
    url: str
