# app/crud.py
from typing import List, Optional
from sqlmodel import select
from sqlmodel import Session
from app.models import Snippet
from datetime import datetime
from app.cache import cache_get, cache_set, cache_delete
import json

def _tags_to_str(tags: Optional[List[str]]) -> Optional[str]:
    if tags is None:
        return None
    return ",".join(t.strip() for t in tags if t)

def _str_to_tags(s: Optional[str]) -> Optional[List[str]]:
    if not s:
        return None
    return [t for t in (x.strip() for x in s.split(",")) if t]

def create_snippet(session: Session, data) -> Snippet:
    snippet = Snippet(
        title=data.title,
        content=data.content,
        category=data.category,
        tags=_tags_to_str(data.tags),
        created_at=datetime.utcnow().isoformat()
    )
    session.add(snippet)
    session.commit()
    session.refresh(snippet)

    # cache it
    cache_set(f"snippet:{snippet.id}", {
        "id": snippet.id,
        "title": snippet.title,
        "content": snippet.content,
        "category": snippet.category,
        "tags": _str_to_tags(snippet.tags),
        "created_at": snippet.created_at,
        "updated_at": snippet.updated_at
    }, ex=600)
    return snippet

def get_snippet(session: Session, snippet_id: int) -> Optional[Snippet]:
    # check cache first
    cached = cache_get(f"snippet:{snippet_id}")
    if cached:
        # return a lightweight object-like dict (crud consumer can return dicts or Pydantic)
        return cached

    snippet = session.get(Snippet, snippet_id)
    if not snippet:
        return None

    obj = {
        "id": snippet.id,
        "title": snippet.title,
        "content": snippet.content,
        "category": snippet.category,
        "tags": _str_to_tags(snippet.tags),
        "created_at": snippet.created_at,
        "updated_at": snippet.updated_at
    }
    cache_set(f"snippet:{snippet.id}", obj, ex=600)
    return obj

def update_snippet(session: Session, snippet_id: int, data) -> Optional[Snippet]:
    snippet = session.get(Snippet, snippet_id)
    if not snippet:
        return None
    if data.title is not None:
        snippet.title = data.title
    if data.content is not None:
        snippet.content = data.content
    if data.category is not None:
        snippet.category = data.category
    if data.tags is not None:
        snippet.tags = _tags_to_str(data.tags)
    snippet.updated_at = datetime.utcnow().isoformat()
    session.add(snippet)
    session.commit()
    session.refresh(snippet)
    # refresh cache
    cache_delete(f"snippet:{snippet_id}")
    return snippet

def delete_snippet(session: Session, snippet_id: int) -> bool:
    snippet = session.get(Snippet, snippet_id)
    if not snippet:
        return False
    session.delete(snippet)
    session.commit()
    cache_delete(f"snippet:{snippet_id}")
    return True

def list_snippets(session: Session, limit: int = 50, offset: int = 0):
    q = select(Snippet).offset(offset).limit(limit).order_by(Snippet.id.desc())
    results = session.exec(q).all()
    # convert tags string to list
    out = []
    for s in results:
        out.append({
            "id": s.id,
            "title": s.title,
            "content": s.content,
            "category": s.category,
            "tags": _str_to_tags(s.tags),
            "created_at": s.created_at,
            "updated_at": s.updated_at
        })
    return out

def search_snippets(session: Session, q_text: str, by_tag: Optional[str] = None, limit: int = 50):
    # Simple search using LIKE on title/content; tag filtering via tags column
    stmt = select(Snippet).where(
        (Snippet.title.ilike(f"%{q_text}%")) | (Snippet.content.ilike(f"%{q_text}%"))
    )
    if by_tag:
        stmt = stmt.where(Snippet.tags.ilike(f"%{by_tag}%"))
    stmt = stmt.limit(limit).order_by(Snippet.id.desc())
    results = session.exec(stmt).all()
    return [
        {
            "id": s.id,
            "title": s.title,
            "content": s.content,
            "category": s.category,
            "tags": _str_to_tags(s.tags),
            "created_at": s.created_at,
            "updated_at": s.updated_at
        }
        for s in results
    ]

def list_tags(session: Session):
    # simple: collect tags from all snippets and return unique set
    stmt = select(Snippet.tags)
    rows = session.exec(stmt).all()
    tagset = set()
    for t in rows:
        if t:
            for tag in (x.strip() for x in t.split(",")):
                if tag:
                    tagset.add(tag)
    return sorted(tagset)
