from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user
from app.routes import task
from app.routes import commentRoutes
import socketio
from app.services.queueService import consume_queue
from app.services.socket import sio
import threading


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
app.include_router(commentRoutes.router, prefix="/api/v1")


# wrap with ASGI application
socket_app = socketio.ASGIApp(sio)

app.mount("/", socket_app)


consumer_thread = threading.Thread(target=consume_queue)
consumer_thread.daemon = (
    True  # This ensures the thread exits when the main program does
)
consumer_thread.start()
