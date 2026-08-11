from fastapi import Request, Depends
from typing import Generator, Iterable
from sqlalchemy.orm import Session
from typing import Callable
from app.database import SessionLocal
from app.exceptions import AuthRequired, Forbidden
from app.utils.jwt import verify_token
from app.services.auth_service import check_role

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

    payload=verify_token(token)
    return payload

def get_current_user_id(payload: dict = Depends(authentication)) -> int:
    return int(payload["sub"])

def authorized(roles: Iterable[str])-> Callable[[int,Session],None]:
    allowed = set(roles)

    def dependency(user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)) -> None:
        role = check_role(db, user_id)
        if role not in allowed:
            raise Forbidden()

    return dependency