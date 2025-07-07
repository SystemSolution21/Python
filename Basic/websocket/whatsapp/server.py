import asyncio

import websockets

# Store connected clients
connected_clients = set()


async def chat_handler(websocket) -> None:
    """Handles an incoming websocket connection.

    Registers the new client, listens for incoming messages, and broadcasts
    them to all other connected clients. Un-registers the client upon
    disconnection.

    Args:
        websocket: The server websocket connection for a client.

    """
    # Register client
    print(f"Client connected: {websocket.remote_address}")
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print(f"Received from {websocket.remote_address}: {message}")
            # Broadcast to all other clients
            other_clients = {
                client for client in connected_clients if client != websocket
            }
            if other_clients:
                print(f"Broadcasting to {len(other_clients)} other client(s).")
                websockets.broadcast(other_clients, message)
            else:
                print("No other clients connected to broadcast to.")
    except websockets.exceptions.ConnectionClosed:
        print(f"Client {websocket.remote_address} disconnected.")
    finally:
        connected_clients.remove(websocket)


async def main() -> None:
    """Starts the websocket chat server and runs it forever."""
    async with websockets.serve(handler=chat_handler, host="localhost", port=8765):
        print("Chat server started on ws://localhost:8765. Press Ctrl+C to stop.")
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shutting down.")
