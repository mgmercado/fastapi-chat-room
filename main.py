from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from frontend.html.ui import HTML
from services.connection_manager import start_chat
import uvicorn

app: FastAPI = FastAPI()


@app.get("/")
async def get() -> HTMLResponse:
    """Returns a simple html ui to interact with the app"""
    return HTMLResponse(HTML)


@app.websocket("/ws/{client_id:int}")
async def websocket_endpoint(websocket: WebSocket, client_id: int) -> None:
    """Handles the websocket connection broadcasting the received text"""
    await start_chat(websocket=websocket, client_id=client_id)

if __name__ == '__main__':
    uvicorn.run("main:app", log_level="info")