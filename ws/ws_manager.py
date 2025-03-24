import asyncio
from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        self.active_connections.remove(ws)

    async def send_personal_message(self, message: dict, ws: WebSocket):
        await ws.send_json(message)

    async def broadcast(self, message: dict, exclude: WebSocket = None):
        tasks = [
            connection.send_json(message)
            for connection in self.active_connections
            if connection != exclude
        ]
        await asyncio.gather(*tasks)