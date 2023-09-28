from fastapi import WebSocket

active_connections: list[WebSocket] = []


async def connect(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)


def disconnect(websocket: WebSocket):
    active_connections.remove(websocket)


async def send_personal_message(message: str, websocket: WebSocket):
    await websocket.send_text(message)


async def broadcast(message: str):
    for connection in active_connections:
        await connection.send_text(message)
