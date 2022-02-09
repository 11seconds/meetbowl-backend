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


@router.post("/users/login", response_model=schemas.Token)
def user_kakao(*, db: Session = Depends(deps.get_db), code: schemas.Code) -> Any:

    get_access_token_headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
    }
    params = {
        "grant_type": "authorization_code",
        "client_id": settings.KAKAO_APP_KEY,
        "redirect_uri": code.redirect_uri,
        "code": code.code,
    }

    kakao_access_token = requests.post(
        "https://kauth.kakao.com/oauth/token",
        headers=get_access_token_headers,
        params=params,
    ).json()
    if not kakao_access_token.get("access_token"):
        raise HTTPException(status_code=401, detail="Incorrect code")

    get_user_info_headers = {
        "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
        "Authorization": "Bearer " + kakao_access_token["access_token"],
    }

    kakao_user = requests.post(
        "https://kapi.kakao.com/v2/user/me", headers=get_user_info_headers
    ).json()

    if not kakao_user.get("id"):
        raise HTTPException(status_code=500, detail="Get kakao id error")

    user = crud.user.get_by_kakao_id(db, kakao_id=kakao_user.get("id"))

    if user:
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

        access_token = schemas.Token(
            access_token=security.create_access_token(
                user.id, expires_delta=access_token_expires
            ),
            token_type="bearer",
        )

        return access_token

    created_user = crud.user.create_by_kakao_id(
        db,
        kakao_id=kakao_user.get("id"),
        nickname=kakao_user.get("properties").get("nickname"),
    )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = schemas.Token(
        access_token=security.create_access_token(
            created_user.id, expires_delta=access_token_expires
        ),
        token_type="bearer",
    )

    return access_token


@router.get("/users/me", response_model=schemas.User)
def get_user_me(
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    본인 유저 정보 조회

    JWT 필요
    """
    return current_user


@router.patch("/users/me", response_model=schemas.User)
def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
    user_in: schemas.UserUpdate,
) -> Any:
    """
    본인 유저 정보 수정

    JWT 필요
    """

    if user_in.nickname is not None and user_in.nickname == "":
        raise HTTPException(status_code=400, detail="Nickname must not be empty string")

    user_db = crud.user.get(db, id=current_user.id)

    if user_db is None:
        raise HTTPException(status_code=404, detail="User not found")

    updated_user = crud.user.update(db, db_obj=user_db, obj_in=user_in)

    return updated_user


@router.get("/timetables/{timetable_id}", response_model=schemas.TimeTable)
def get_timetable_by_id(timetable_id: str, db: Session = Depends(deps.get_db)) -> Any:
    """
    타임테이블 정보 보기
    """
    timetables = crud.timetable.get(db, id=timetable_id)
    if timetables is None:
        raise HTTPException(status_code=404, detail="Timetable not found")
    return timetables


@router.get(
    "/timetables/{timetable_id}/scheduleblocks",
    response_model=List[schemas.ScheduleBlock],
)
def get_scheduleblocks_by_timetable_id(
    timetable_id: str, db: Session = Depends(deps.get_db)
) -> Any:
    """
    타임테이블의 스케쥴 블록 조회
    """
    scheduleblock = crud.scheduleblock.get_all(db, table_id=timetable_id)
    return scheduleblock


@router.get(
    "/timetables/{timetable_id}/scheduleblocks/me",
    response_model=List[schemas.ScheduleBlock],
)
def get_my_scheduleblocks_by_timetable_id(
    timetable_id: str,
    db: Session = Depends(deps.get_db),
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    로그인한 유저 본인의 타임테이블의 스케쥴 블록 조회
    """
    scheduleblocks = crud.scheduleblock.get_all_by_user_id(
        db, table_id=timetable_id, user_id=current_user.id
    )
    return scheduleblocks


@router.post("/timetables", response_model=schemas.TimeTable, status_code=201)
def create_timetable(
    *,
    db: Session = Depends(deps.get_db),
    timetable_in: schemas.TimeTableCreate,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """
    타임테이블 생성
    """
    timetable = crud.timetable.create_with_user_id(
        db, obj_in=timetable_in, user_id=current_user.id
    )
    if not timetable:
        raise HTTPException(status_code=500, detail="Timetable is not created")
    return timetable


@router.patch(
    "/timetables/{timetable_id}", response_model=schemas.TimeTable, status_code=201
)
def update_timetable_by_id(
    *,
    db: Session = Depends(deps.get_db),
    timetable_id: str,
    timetable_in: schemas.TimeTableUpdate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    시간표 정보 수정
    JWT 필요
    """
    timetable_db = crud.timetable.get(db, timetable_id)

    if timetable_db is None:
        raise HTTPException(status_code=404, detail="Timetable not found")

    if timetable_db.create_user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="The user doesn't have enough privileges. Only timetable owner can update info.",
        )

    return_timetable = crud.timetable.update(
        db, db_obj=timetable_db, obj_in=timetable_in
    )
    return return_timetable


@router.post("/scheduleblocks", status_code=201, response_model=schemas.ScheduleBlock)
def create_scheduleblock(
    *,
    db: Session = Depends(deps.get_db),
    scheduleblock_in: schemas.ScheduleBlockCreate,
    current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    스케쥴 블록 생성 API
    """
    scheduleblock = crud.scheduleblock.create_with_user_id(
        db, obj_in=scheduleblock_in, user_id=current_user.id
    )

    return scheduleblock


@router.patch("/scheduleblocks", status_code=201)
def update_scheduleblock_by_id(
    *,
    db: Session = Depends(deps.get_db),
    scheduleblocks_in: List[schemas.ScheduleBlockUpdate],
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    """ 스케쥴 블록 수정
    JWT 필요
    """

    scheduleblocks: List[scheduleblock.ScheduleBlock] = []

    for scheduleblock_in in scheduleblocks_in:
        scheduleblock_db = crud.scheduleblock.get(db, id=scheduleblock_in.id)

        if scheduleblock_db is None:
            raise HTTPException(status_code=404, detail="Scheduleblock not found")

        if scheduleblock_db.user_id != current_user.id:
            raise HTTPException(
                status_code=403, detail="The user doesn't have enough privileges"
            )

        updated_scheduleblock = crud.scheduleblock.update(
            db, db_obj=scheduleblock_db, obj_in=scheduleblock_in
        )

        scheduleblocks.append(updated_scheduleblock)
    return scheduleblocks


@router.delete("/scheduleblocks/{scheduleblock_id}")
def delete_scheduleblock_by_id(
    scheduleblock_id: str,
    db: Session = Depends(deps.get_db),
    *,
    current_user: schemas.User = Depends(deps.get_current_user),
) -> Any:
    scheduleblock_db = crud.scheduleblock.get(db, id=scheduleblock_id)

    if scheduleblock_db is None:
        raise HTTPException(status_code=404, detail="Scheduleblock not found")

    if scheduleblock_db.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )

    _return = crud.scheduleblock.remove(db, id=scheduleblock_db.id)

    return _return


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
