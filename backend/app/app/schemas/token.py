from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class Code(BaseModel):
    code: str
    redirect_uri: str


class Authorization(BaseModel):
    Authorization: str