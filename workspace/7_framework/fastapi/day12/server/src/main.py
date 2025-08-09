from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# Create the FastAPI app instance
app = FastAPI()

@app.get("/")
def read_root():
    """
    A simple root endpoint to confirm the API is running.
    """
    return {"status": "API is running"}

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int):
    """
    This endpoint handles WebSocket connections for the chat room.
    """
    await manager.connect(websocket)
    await manager.broadcast(f"Client #{client_id} has entered the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Client #{client_id}: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")
