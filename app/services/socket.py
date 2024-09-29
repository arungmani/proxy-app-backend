import socketio

# Initialize the Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi",)


# Define event handlers in this module or other parts of the code can add more handlers.
@sio.event
async def connect(sid, environ):

    await sio.emit(
        "a_new_event",
    )
    await list_connected_clients()


@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")
    await list_connected_clients()


# You can define more events here as needed...


async def list_connected_clients():
    # Get the list of all connected client session IDs
    connected_clients = sio.manager.rooms["/"]  # Default namespace ('/')

    print("Connected clients:")
    for sid in connected_clients:
        print(f"Client {sid} is connected")


async def broadcast_message(data):
    """Async function to emit the notification."""
    await sio.emit(
        "task_notification",
        {"message": f"New task {data['task_name']} added by {data['user']}"},
        broadcast=True,
        skip_sid=data['sid'],  # Ensure 'sid' is part of your message
    )