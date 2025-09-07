# app/schemas.py
from typing import Optional, List
from pydantic import BaseModel

class SnippetCreate(BaseModel):
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class SnippetUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[List[str]] = None

class SnippetRead(BaseModel):
    id: int
    title: str
    content: str
    category: Optional[str] = None
    tags: Optional[List[str]] = None
    created_at: str
    updated_at: Optional[str] = None

    class Config:
        orm_mode = True
