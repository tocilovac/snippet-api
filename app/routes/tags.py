# app/routes/tags.py
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app import crud

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("/")
def get_tags(session: Session = Depends(get_session)):
    return {"tags": crud.list_tags(session)}
