from app.database import SessionLocal
from fastapi import Request
from app.exceptions import AuthRequired
from app.utils.jwt import verify_token
from typing import Union

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def authentication(request: Request)->dict[str:Union[str,int]]:
    token = request.cookies.get("access_token")
    if not token:
        raise AuthRequired()

    return verify_token(token)