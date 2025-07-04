import asyncio

import websockets


async def send(websocket) -> None:
    """Handles sending messages from the user to the websocket server.

    Reads user input from the console and sends it over the websocket.
    The loop breaks if the user types 'exit'.

    Args:
        websocket: The client websocket connection.

    """
    while True:
        msg: str = await asyncio.to_thread(input, "You: ")
        if msg.lower() == "exit":
            await websocket.close()
            break
        await websocket.send(msg)


async def receive(websocket) -> None:
    """Handles receiving messages from the websocket server and printing them.

    Listens for incoming messages and prints them to the console.
    Handles server disconnection gracefully.

    Args:
        websocket: The client websocket connection.

    """
    try:
        async for message in websocket:
            print(f"\nFriend: {message}\nYou: ", end="")
    except websockets.exceptions.ConnectionClosed:
        print("Disconnected from server.")


async def main() -> None:
    """The main coroutine that connects to the websocket server.

    Establishes a connection and runs the send and receive tasks concurrently.

    """
    uri = "ws://localhost:8765"
    async with websockets.connect(uri=uri) as websocket:
        print("Connected to chat. Type 'exit' to quit.")
        await asyncio.gather(send(websocket), receive(websocket))


if __name__ == "__main__":
    asyncio.run(main())
