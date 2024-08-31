import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, AsyncGenerator
from repositories import PostgresRepository

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = PostgresRepository(
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
)

async def lifespan(app: FastAPI) -> AsyncGenerator:
    """Lifespan context manager to manage startup and shutdown events."""
    await repo.connect()
    yield
    await repo.close()

app = FastAPI(lifespan=lifespan)

@app.post("/api/post")
async def post_message(data: Dict[str, Any]) -> Dict[str, str]:
    return {"message": f"Hello from the POST endpoint! You sent: {data['username']}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3000)