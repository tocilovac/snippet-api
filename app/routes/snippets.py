from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from app.database import get_session
from app.schemas import SnippetCreate, SnippetRead, SnippetUpdate
from app import crud

router = APIRouter(prefix="/snippets", tags=["snippets"])

@router.post("/", response_model=SnippetRead, status_code=status.HTTP_201_CREATED)
def create(payload: SnippetCreate, session: Session = Depends(get_session)):
    return crud.create_snippet(session, payload)

@router.get("/{snippet_id}", response_model=SnippetRead)
def read(snippet_id: int, session: Session = Depends(get_session)):
    snippet = crud.get_snippet(session, snippet_id)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet

@router.put("/{snippet_id}", response_model=SnippetRead)
def update(snippet_id: int, payload: SnippetUpdate, session: Session = Depends(get_session)):
    snippet = crud.update_snippet(session, snippet_id, payload)
    if not snippet:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return snippet

@router.delete("/{snippet_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete(snippet_id: int, session: Session = Depends(get_session)):
    ok = crud.delete_snippet(session, snippet_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Snippet not found")
    return None

@router.get("/", response_model=List[SnippetRead])
def list_all(limit: int = 50, offset: int = 0, session: Session = Depends(get_session)):
    return crud.list_snippets(session, limit=limit, offset=offset)
