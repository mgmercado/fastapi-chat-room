from fastapi import WebSocket, WebSocketDisconnect

active_connections: list[WebSocket] = []


async def connect(websocket: WebSocket) -> None:
    """Accepts websocket connection"""
    await websocket.accept()
    active_connections.append(websocket)


def disconnect(websocket: WebSocket) -> None:
    """Removes a given websocket from the pool"""
    active_connections.remove(websocket)


async def send_personal_message(message: str, websocket: WebSocket) -> None:
    """Sends text to the given websocket"""
    await websocket.send_text(message)


async def broadcast(message: str) -> None:
    """Sends text to all active connections"""
    for connection in active_connections:
        await connection.send_text(message)


async def start_chat(websocket: WebSocket, client_id: int) -> None:
    """Establishes websocket connection and broadcasts chat messages"""
    await connect(websocket)
    try:
        while True:
            data: str = await websocket.receive_text()
            await send_personal_message(f"You wrote: {data}", websocket)
            await broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        disconnect(websocket)
        await broadcast(f"Client #{client_id} has left the chat")
