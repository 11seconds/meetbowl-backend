from pydantic import BaseModel


class KakaoUser(BaseModel):
    id: int
