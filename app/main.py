from fastapi import FastAPI
from app.routes import item

app = FastAPI(
    title="FastAPI with MongoDB",
    description="A simple FastAPI application with MongoDB integration",
    version="1.0.0"
)

app.include_router(item.router, prefix="/api/v1")