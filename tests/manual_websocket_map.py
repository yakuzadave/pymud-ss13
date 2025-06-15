import asyncio
import json
import websockets


async def main():
    uri = "ws://localhost:5000/ws"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"type": "map_request"}))
        print("sent map_request")
        msg = await ws.recv()
        print("received:", msg)


if __name__ == "__main__":
    asyncio.run(main())
