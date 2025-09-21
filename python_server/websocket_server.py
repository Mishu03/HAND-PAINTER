import asyncio
import websockets
import json

# Connected clients
clients = set()

async def handler(websocket):
    # Register client
    clients.add(websocket)
    print("Client connected")
    try:
        async for message in websocket:
            # For this server, we just broadcast received messages to all clients
            data = message
            # Optionally, you can parse JSON:
            # data = json.loads(message)
            for client in clients:
                if client != websocket:
                    await client.send(data)
    except websockets.exceptions.ConnectionClosed:
        print("Client disconnected")
    finally:
        clients.remove(websocket)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("WebSocket server running on ws://localhost:8765")
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())