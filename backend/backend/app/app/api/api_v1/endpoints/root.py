from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException


router = APIRouter()


@router.get("/")
def root():
    return "hello world!"
