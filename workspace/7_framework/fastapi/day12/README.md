# FastAPI Day 12: Real-Time Chat with WebSockets

Welcome to **Day 12** of the FastAPI tutorial series! Today, we're diving into the world of real-time communication with WebSockets. You'll learn how to build a simple chat application where multiple clients can connect and exchange messages in real-time.

---

## What You'll Learn

-   **WebSocket Endpoints**: Implement a WebSocket endpoint in FastAPI to handle persistent connections.
-   **Connection Management**: Create a `ConnectionManager` to keep track of active WebSocket connections.
-   **Broadcasting Messages**: Broadcast messages to all connected clients to enable real-time chat functionality.
-   **Client-Side Integration**: Build a simple HTML and JavaScript client to interact with your WebSocket server.
-   **Testing WebSockets**: Write tests for your WebSocket endpoint using `pytest` and FastAPI's `TestClient`.

---

## Key Concepts

For this tutorial, we've built a simple chat server with a corresponding client.

-   `src/main.py`: Contains the main FastAPI application, the `ConnectionManager`, and the WebSocket endpoint.
-   `client/index.html`: A simple HTML file with JavaScript to connect to the WebSocket and handle messaging.
-   `tests/test_main.py`: Contains tests for the WebSocket endpoint.

### 1. The Connection Manager

To manage all active WebSocket connections, we use a `ConnectionManager` class. This class is responsible for adding new connections, removing disconnected ones, and broadcasting messages to all clients.

```python-beginner/workspace/7_framework/fastapi/day12/server/src/main.py#L4-L18
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
```

### 2. The WebSocket Endpoint

The core of our application is the WebSocket endpoint, defined with the `@app.websocket()` decorator. This endpoint handles incoming connections, listens for messages, and broadcasts them to all other clients.

```python-beginner/workspace/7_framework/fastapi/day12/server/src/main.py#L26-L38
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
```

### 3. Client-Side Implementation

The `client/index.html` file provides a simple user interface for the chat. It uses JavaScript's `WebSocket` API to connect to the server, send messages, and display received messages.

```python-beginner/workspace/7_framework/fastapi/day12/client/index.html#L48-L69
<script>
    var clientId = Date.now();
    document.querySelector("#ws-id").textContent = clientId;
    var ws = new WebSocket(`ws://localhost:8000/ws/${clientId}`);
    ws.onmessage = function (event) {
        var messages = document.getElementById("messages");
        var message = document.createElement("li");
        var content = document.createTextNode(event.data);
        message.appendChild(content);
        messages.appendChild(message);
        messages.scrollTop = messages.scrollHeight;
    };
    function sendMessage(event) {
        var input = document.getElementById("messageText");
        ws.send(input.value);
        input.value = "";
        event.preventDefault();
    }
</script>
```

### 4. Testing WebSockets

Testing WebSockets is straightforward with FastAPI's `TestClient`. We can use `client.websocket_connect()` to simulate a client connection and test the message flow.

```python-beginner/workspace/7_framework/fastapi/day12/server/tests/test_main.py#L14-L32
def test_websocket_broadcast(client):
    """
    Test the WebSocket broadcasting functionality.
    - It connects two clients to the /ws/{client_id} endpoint.
    - It checks the initial connection messages in the correct order.
    - Has one client send a message.
    - Asserts that both clients receive the broadcasted message.
    """
    with client.websocket_connect("/ws/1") as websocket1:
        # Client 1 connects and receives its own connection message
        assert websocket1.receive_text() == "Client #1 has entered the chat"

        with client.websocket_connect("/ws/2") as websocket2:
            # Client 2 connects, and both clients receive the announcement
            assert websocket1.receive_text() == "Client #2 has entered the chat"
            assert websocket2.receive_text() == "Client #2 has entered the chat"

            # Test broadcasting a message from client 1
            websocket1.send_text("Hello from client 1")
            assert websocket1.receive_text() == "Client #1: Hello from client 1"
            assert websocket2.receive_text() == "Client #1: Hello from client 1"
```

---

## Next Steps

-   Navigate to the server directory and install the dependencies: `cd server && pip install -r requirements.txt`.
-   Run the application with `uvicorn src.main:app --reload`.
-   Open `client/index.html` in your web browser. You can open multiple tabs to simulate multiple clients.
-   Send messages and see them appear in all open tabs.
-   Run the automated tests with `python -m pytest`.

---