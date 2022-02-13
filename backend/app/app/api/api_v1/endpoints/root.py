from datetime import timedelta
from typing import Any, List

import requests
from fastapi import APIRouter, Depends, HTTPException, WebSocket
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.core import security
from app.core.config import settings
from app.models import scheduleblock

router = APIRouter()

# 개발할 때 여기서 모든 API 만들고 나중에 모듈화 진행할 예정임


html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost/api/v1/ws/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@router.get("/")
def root() -> HTMLResponse:
    """
    웹소켓 테스트용 프론트
    """
    return HTMLResponse(html)


class ConnectionManager:
    def __init__(self) -> None:
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, timetable_id: str) -> None:
        await websocket.accept()
        self.connections.append(websocket)

    def disconnect(self, websocket: WebSocket) -> None:
        self.connections.append(websocket)

    async def send_message_by_id(self, websocket: WebSocket, message: str) -> None:
        await websocket.send_text(message)

    async def send_message_to_all(self, timetable_id: str, message: str) -> None:
        for connection in self.connections:
            await connection.send_text(f"{timetable_id}: {message}")


manager = ConnectionManager()


@router.websocket("/ws/{timetable_id}")
async def ws_connect(websocket: WebSocket, timetable_id: str) -> None:
    await manager.connect(websocket=websocket, timetable_id=timetable_id)
    try:
        while True:
            # 여기에 다른 사람의 제출을 기다렸다가 쏴주는 로직이 필요함 근데 db에 저장되고 call을 할 수 있을까?
            # db 저장시 lock이 걸려도 괜찮을까?
            # 방장에게만 쏴주어도 될까? 전체에게 쏴주어야 할까?
            data = await websocket.receive_text()
            await manager.send_message_to_all(timetable_id, data)

    except Exception:
        manager.disconnect(websocket)
