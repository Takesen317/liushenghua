"""
Task schemas
"""
from pydantic import BaseModel, ConfigDict
from typing import Optional


class TaskCreate(BaseModel):
    file_id: str
    style: str = "warm"
    voice: str = "xiaoxiao"
    music_style: str = "gentle"


class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    user_id: str
    file_id: str
    status: str
    progress: int
    current_step: Optional[str]
    style: str
    voice: str
    music_style: str
    ai_description: Optional[str]
    result_data: Optional[dict]
    error_message: Optional[str]
    created_at: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    progress: int
    current_step: Optional[str]
    result: Optional[dict]
