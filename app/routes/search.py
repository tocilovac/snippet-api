# app/routes/search.py
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session
from typing import Optional
from app.database import get_session
from app import crud

router = APIRouter(prefix="/search", tags=["search"])

@router.get("/snippets")
def search_snippets(q: str = Query(..., min_length=1), tag: Optional[str] = None, limit: int = 50, session: Session = Depends(get_session)):
    results = crud.search_snippets(session, q_text=q, by_tag=tag, limit=limit)
    return {"results": results}
