import socketio

# Initialize the Socket.IO server
sio = socketio.AsyncServer(
    cors_allowed_origins="*",
    async_mode="asgi",
)


# Define event handlers in this module or other parts of the code can add more handlers.
@sio.event
async def connect(sid, environ):
    await list_connected_clients()


@sio.event
async def disconnect(sid):
    print(f"Client {sid} disconnected")
    await list_connected_clients()


async def handleJoinRoomEvent(sid, data):
    print("h121263237012", data["user_id"])
    room = data["user_id"]
    res=sio.enter_room(sid,room)
    print(f"Client {sid} joined room",res)


sio.on("join_room", handleJoinRoomEvent)


def get_all_rooms():
    # Check if the namespace exists in sio.manager.rooms
    if "/" not in sio.manager.rooms:
        print("No rooms available yet.")
        return []

    # Get all room names
    all_rooms = sio.manager.rooms["/"]

    # Filter out individual client rooms by ignoring the `sid` keys
    named_rooms = [room for room in all_rooms if not isinstance(room, str) or not room.startswith("sid:")]
    return named_rooms

# Call the function after ensuring sio has been initialized


async def send_message_to_room(room, message):
    await sio.emit("room_message", {"message": message}, room=room)
    print(f"Message sent to room {room}: {message}")


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
        data,
        broadcast=True,
        skip_sid=data["sid"],  # Ensure 'sid' is part of your message
    )
    return 
