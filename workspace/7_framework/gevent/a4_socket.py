# Socket Programming

import gevent
from gevent import socket

def tcp_server(port):
    """
    Simple TCP server that handles multiple clients concurrently
    """
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind(('localhost', port))
        server_socket.listen(5)
        print(f"Server listening on port {port}")

        while True:
            # Accept connections (this will yield to other greenlets)
            client_socket, address = server_socket.accept()
            print(f"Connection from {address}")

            # Handle each client in a separate greenlet
            gevent.spawn(handle_client, client_socket, address)

    except KeyboardInterrupt:
        print("Server shutting down...")
    finally:
        server_socket.close()

def handle_client(client_socket, address):
    """
    Handle individual client connections
    """
    try:
        while True:
            # Receive data (non-blocking thanks to gevent)
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8').strip()
            print(f"Received from {address}: {message}")

            # Echo the message back
            response = f"Echo: {message}\n"
            client_socket.send(response.encode('utf-8'))

    except Exception as e:
        print(f"Error handling client {address}: {e}")
    finally:
        client_socket.close()
        print(f"Connection with {address} closed")

def tcp_client(port, client_id):
    """
    Simple TCP client for testing
    """
    client_socket = None
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('localhost', port))

        for i in range(3):
            message = f"Message {i+1} from client {client_id}"
            client_socket.send(message.encode('utf-8'))

            response = client_socket.recv(1024)
            print(f"Client {client_id} received: {response.decode('utf-8').strip()}")

            gevent.sleep(1)  # Wait between messages

    except Exception as e:
        print(f"Client {client_id} error: {e}")
    finally:
        if client_socket:
            client_socket.close()

# Note: Run server in one terminal and clients in another, or use threading

# Start server in background
server_greenlet = gevent.spawn(tcp_server, 12345)
gevent.sleep(1)  # Give server time to start

# Start multiple clients
client_greenlets = [
    gevent.spawn(tcp_client, 12345, f"Client-{i}")
    for i in range(3)
]

# Wait for clients to finish
gevent.joinall(client_greenlets, timeout=15)
server_greenlet.kill()  # Stop server
