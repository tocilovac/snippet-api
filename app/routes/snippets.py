# app/routes/snippets.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.schemas import SnippetCreate, SnippetRead, SnippetUpdate
from app import crud

router = APIRouter(prefix="/snippets", tags=["snippets"])

@router.post("/", response_model=SnippetRead, status_code=status.HTTP_201_CREATED)
def create(payload: SnippetCreate, session: Session = Depends(get_session)):
    s = crud.create_snippet(session, payload)
    return SnippetRead.model_validate(s)

@router.get("/{snippet_id}", response_model=SnippetRead)
def read(snippet_id: int, session: Session = Depends(get_session)):
    s = crud.get_snippet(session, snippet_id)
    if not s:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return SnippetRead.model_validate(s)

@router.put("/{snippet_id}", response_model=SnippetRead)
def update(snippet_id: int, payload: SnippetUpdate, session: Session = Depends(get_session)):
    s = crud.update_snippet(session, snippet_id, payload)
    if not s:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return SnippetRead.model_validate(s)

@router.delete("/{snippet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(snippet_id: int, session: Session = Depends(get_session)):
    ok = crud.delete_snippet(session, snippet_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return None

@router.get("/", response_model=List[SnippetRead])
def list_all(limit: int = 50, offset: int = 0, session: Session = Depends(get_session)):
    snippets = crud.list_snippets(session, limit=limit, offset=offset)
    return [SnippetRead.model_validate(s) for s in snippets]
