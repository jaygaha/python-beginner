import pytest
from fastapi.testclient import TestClient
from src.main import app

@pytest.fixture
def client():
    """
    Pytest fixture to create a TestClient for our app.
    """
    return TestClient(app)

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
