from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user
from app.routes import task
from app.routes import comments
import socketio
from app.services.queueService import consume_queue
from app.services.socket import sio
from app.services.redisService import client
import threading
from app.services.email_service import sendEmail
import os
from app.db.database import initialize_indexes
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from fastapi.responses import FileResponse


app = FastAPI(
    title="FastAPI with MongoDB",
    description="A simple FastAPI application with MongoDB integration",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router, prefix="/api/v1")
app.include_router(task.router, prefix="/api/v1")
app.include_router(comments.router, prefix="/api/v1")


# Serve the main index.html for SPA routing
@app.get("/")
async def checkTest(request: Request):

    return "Hello from API route"


# wrap with ASGI application
socket_app = socketio.ASGIApp(sio)

app.mount("/", socket_app)


consumer_thread = threading.Thread(target=consume_queue)
consumer_thread.daemon = (
    True  # This ensures the thread exits when the main program does
)
consumer_thread.start()


@app.on_event("startup")
async def startup_db_client():
    await initialize_indexes()
