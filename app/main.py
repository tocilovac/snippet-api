from fastapi import FastAPI
from app.database import init_db  # ✅ Correct import
from app.routes import snippets, tags, search  # ✅ Also fix this if needed
import redis

app = FastAPI(
    title="Knowledge Snippet API",
    version="0.1.0",
    description="Save and search bite-sized knowledge snippets"
)

# Redis connection
redis_client = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

@app.on_event("startup")
def on_startup():
    init_db()

# Include your existing routers
app.include_router(snippets.router)
app.include_router(tags.router)
app.include_router(search.router)

@app.get("/", tags=["root"])
def root():
    return {"message": "Knowledge Snippet API up and running"}

# 🔴 Add data to Redis
@app.post("/redis/add/{key}/{value}", tags=["redis"])
def add_to_redis(key: str, value: str):
    redis_client.set(key, value)
    return {"message": f"Stored {key} = {value}"}

# 🟢 Read data from Redis
@app.get("/redis/read/{key}", tags=["redis"])
def read_from_redis(key: str):
    value = redis_client.get(key)
    if value:
        return {"key": key, "value": value}
    return {"error": "Key not found"}
