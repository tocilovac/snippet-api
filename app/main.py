from fastapi import FastAPI
from app.database import init_db  # ✅ Correct import
from app.routes import snippets, tags, search  # ✅ Also fix this if needed

app = FastAPI(
    title="Knowledge Snippet API",
    version="0.1.0",
    description="Save and search bite-sized knowledge snippets"
)

@app.on_event("startup")
def on_startup():
    init_db()  # ✅ Now this will work

app.include_router(snippets.router)
app.include_router(tags.router)
app.include_router(search.router)

@app.get("/", tags=["root"])
def root():
    return {"message": "Knowledge Snippet API up and running"}
