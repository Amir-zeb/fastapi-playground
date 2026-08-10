from fastapi import Request
from app.database import SessionLocal
from app.exceptions import AuthRequired
from app.utils.jwt import verify_token
from typing import Generator
from sqlalchemy.orm import Session

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

def authentication(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise AuthRequired()

    return verify_token(token)