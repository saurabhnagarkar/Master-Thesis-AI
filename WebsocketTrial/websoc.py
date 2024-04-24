import asyncio
import websockets
import aioconsole

async def handler(websocket, path):
    print("Client connected.")
    
    async def send_messages():
        while True:
            message = await aioconsole.ainput("Enter message to send to C#: ")
            await websocket.send(message)
            print(f"Sent: {message}")

    async def receive_messages():
        async for message in websocket:
            print(f"Message from C#: {message}")

    send_task = asyncio.create_task(send_messages())
    receive_task = asyncio.create_task(receive_messages())
    await asyncio.gather(send_task, receive_task)

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("Server started, waiting for connections...")
        await asyncio.Future()

asyncio.run(main())
