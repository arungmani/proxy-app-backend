from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user
from app.routes import task

app = FastAPI(
    title="FastAPI with MongoDB",
    description="A simple FastAPI application with MongoDB integration",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user.router, prefix="/api/v1")
app.include_router(task.router, prefix="/api/v1")