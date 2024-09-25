import socketio

# Initialize the Socket.IO server
sio = socketio.AsyncServer(cors_allowed_origins="*", async_mode="asgi")


# Define event handlers in this module or other parts of the code can add more handlers.
@sio.event
async def connect(sid, environ):
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


