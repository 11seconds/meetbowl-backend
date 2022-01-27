from typing import Any, List, Dict

from fastapi import APIRouter, Depends, HTTPException, WebSocket

from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.models import timetable, scheduleblock, user


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
def root():
    """
    웹소켓 테스트용 프론트
    """
    return HTMLResponse(html)


@router.get("/user/login")
def user_kakao(*, db: Session, code: str):
    return ""


@router.get("/timetables/{timetable_id}", response_model=schemas.TimeTable, response_model_exclude_unset=True)
def get_timetable_by_id(
    timetable_id: str,
    db: Session = Depends(deps.get_db)
):
    """
    타임테이블 정보 보기
    """
    timetables = crud.timetable.get(db, id=timetable_id)
    return timetables


@router.post("/users/join", response_model=schemas.User)
def user_join(*, db: Session = Depends(deps.get_db), user_in: schemas.UserCreate):
    """
    유저 생성 API -> 유저 아이디 반환
    
    유저 아이디 값으로 vailidation 합니다.
    
    password, email은 선택입니다.
    """
    user = crud.user.create(db, obj_in=user_in)
    return user
    


@router.get("/timetables/{timetable_id}/scheduleblocks")
def get_scheduleblocks_by_timetable_id(
    timetable_id: str,
    db: Session = Depends(deps.get_db)
):
    """
    타임테이블의 스케쥴 블록 조회
    """
    scheduleblock = crud.scheduleblock.get_all(db, table_id=timetable_id)
    return scheduleblock


@router.post("/timetable", response_model=schemas.TimeTable, response_model_exclude_unset=True)
def create_timetable(
    *,
    db: Session = Depends(deps.get_db),
    timetable_in: schemas.TimeTableCreate
):
    timetable = crud.timetable.create(db, obj_in=timetable_in)
    return timetable


@router.put("/timetable")
def update_timetable_by_id(
    *,
    timetable_id: str,
    db: Session = Depends(deps.get_db),
    timetable_in: schemas.TimeTableUpdate
):
    """
    시간표 정보 수정
    """
    timetable = crud.timetable.update(db, obj_in=timetable_in)
    return timetable



@router.post("/scheduleblock")
def create_scheduleblock(
    *,
    db: Session = Depends(deps.get_db),
    scheduleblock_in: schemas.ScheduleBlockCreate
):
    """
    스케쥴 블록 생성 API
    """
    scheduleblock = crud.scheduleblock.create(db, obj_in=scheduleblock_in)
    return scheduleblock


@router.put("/scheduleblock")
def update_scheduleblock_by_id(
    *,
    db: Session = Depends(deps.get_db),
    scheduleblock_in: schemas.ScheduleBlockUpdate
):
    """ 스케쥴 블록 수정
    """
    scheduleblock = crud.scheduleblock.update(db, obj_in=scheduleblock_in)
    return scheduleblock


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []
        
    async def connect(self, websocket: WebSocket, timetable_id: str):
        await websocket.accept()
        self.connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.connections.append(websocket)
        
    async def send_message_by_id(self, websocket: WebSocket, message: str):
        await websocket.send_text(message)

    async def send_message_to_all(self, timetable_id: str ,message: str):
        for connection in self.connections:
            await connection.send_text(f"{timetable_id}: {message}")


manager = ConnectionManager()


@router.websocket("/ws/{timetable_id}")
async def ws_connect(websocket: WebSocket, timetable_id: str):
    await manager.connect(websocket=websocket, timetable_id=timetable_id)
    try:
        while True:
            # 여기에 다른 사람의 제출을 기다렸다가 쏴주는 로직이 필요함 근데 db에 저장되고 call을 할 수 있을까?
            # db 저장시 lock이 걸려도 괜찮을까?
            # 방장에게만 쏴주어도 될까? 전체에게 쏴주어야 할까?
            data = await websocket.receive_text()
            await manager.send_message_to_all(timetable_id, data)
    
    except Exception as e:
        manager.disconnect(websocket)
