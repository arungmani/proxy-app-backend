from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import user
from app.routes import task
import socketio
from app.services.queueService import add_data
from app.services.queueService import consume_queue


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

sio = socketio.AsyncServer(cors_allowed_origins='*',async_mode='asgi')

#wrap with ASGI application
socket_app = socketio.ASGIApp(sio)

app.mount("/", socket_app)


# Socket.IO event handlers
@sio.event
async def connect(sid, environ):
    print(f"Client {sid} connected")

@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")



@sio.event
async def create_task(sid, task_data):
    print(f"Task created by {sid}: {task_data}")
    # Broadcast the task creation to all clients
    await sio.emit('task_notification', task_data, broadcast=True)