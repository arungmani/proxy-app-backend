from fastapi import FastAPI
from app.routes import item
from app.routes import user
from app.routes import task

app = FastAPI(
    title="FastAPI with MongoDB",
    description="A simple FastAPI application with MongoDB integration",
    version="1.0.0"
)

app.include_router(item.router, prefix="/api/v1")
app.include_router(user.router, prefix="/api/v1")
app.include_router(task.router, prefix="/api/v1")