from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from frontend.html.ui import HTML
from services import connection_manager

app = FastAPI()


@app.get("/")
async def get():
    return HTMLResponse(HTML)


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    await connection_manager.connect(websocket)
    try:
        while True:
            data: str = await websocket.receive_text()
            await connection_manager.send_personal_message(f"You wrote: {data}", websocket)
            await connection_manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        connection_manager.disconnect(websocket)
        await connection_manager.broadcast(f"Client #{client_id} has left the chat")
