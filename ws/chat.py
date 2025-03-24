from ws.ws_manager import ConnectionManager
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request

from fastapi import APIRouter

from fastapi import WebSocket, WebSocketDisconnect

router = APIRouter()

conn_manager = ConnectionManager()

templates = Jinja2Templates(directory="templates")

@router.get("/chatroom/{username}")
async def ohatroom_page_endpoint(request: Request, username: str) -> HTMLResponse: 
    return templates.TemplateResponse(request=request, name="chatroom.html", context={"username": username})


@router.websocket("/chatroom/{username}")
async def chatroom_endpoint(websocket: WebSocket, username: str):
    await conn_manager.connect(websocket)
    await conn_manager.broadcast({"pizda": f"{username} joined the chat"}, exclude=websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await conn_manager.broadcast({"sender": f"{username}", "message": data}, websocket, )
    except WebSocketDisconnect:
        conn_manager.disconnect(websocket)
        await conn_manager.broadcast({"sender": "system", "message": f"Client #{username} left the chat",})
