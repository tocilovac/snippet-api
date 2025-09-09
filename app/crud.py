from typing import Optional, List
from sqlmodel import Session
from datetime import datetime
from app.models import Snippet
from app.schemas import SnippetRead
from app.cache import cache_get, cache_set, cache_delete

def _tags_to_str(tags: Optional[List[str]]) -> Optional[str]:
    return ",".join(tags) if tags else None

def _str_to_tags(s: Optional[str]) -> Optional[List[str]]:
    return s.split(",") if s else None

def create_snippet(session: Session, data) -> SnippetRead:
    snippet = Snippet(
        title=data.title,
        content=data.content,
        category=data.category,
        tags=_tags_to_str(data.tags),
        created_at=datetime.utcnow()
    )
    session.add(snippet)
    session.commit()
    session.refresh(snippet)

    snippet_dict = {
        "id": snippet.id,
        "title": snippet.title,
        "content": snippet.content,
        "category": snippet.category,
        "tags": _str_to_tags(snippet.tags),
        "created_at": snippet.created_at,
        "updated_at": snippet.updated_at
    }
    cache_set(f"snippet:{snippet.id}", snippet_dict, ex=600)
    return SnippetRead.model_validate(snippet_dict)

def get_snippet(session: Session, snippet_id: int) -> Optional[SnippetRead]:
    cached = cache_get(f"snippet:{snippet_id}")
    if cached:
        return SnippetRead.model_validate(cached)

    snippet = session.get(Snippet, snippet_id)
    if not snippet:
        return None

    snippet_dict = {
        "id": snippet.id,
        "title": snippet.title,
        "content": snippet.content,
        "category": snippet.category,
        "tags": _str_to_tags(snippet.tags),
        "created_at": snippet.created_at,
        "updated_at": snippet.updated_at
    }
    cache_set(f"snippet:{snippet.id}", snippet_dict, ex=600)
    return SnippetRead.model_validate(snippet_dict)

def update_snippet(session: Session, snippet_id: int, data) -> Optional[SnippetRead]:
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

    snippet.updated_at = datetime.utcnow()
    session.add(snippet)
    session.commit()
    session.refresh(snippet)

    cache_delete(f"snippet:{snippet_id}")

    snippet_dict = {
        "id": snippet.id,
        "title": snippet.title,
        "content": snippet.content,
        "category": snippet.category,
        "tags": _str_to_tags(snippet.tags),
        "created_at": snippet.created_at,
        "updated_at": snippet.updated_at
    }
    return SnippetRead.model_validate(snippet_dict)
