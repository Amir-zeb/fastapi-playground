from fastapi import Request, Depends
from typing import Iterable, Callable, AsyncGenerator, Coroutine, Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.rate_limiter import is_rate_limited
from app.database import SessionLocal
from app.exceptions import AuthRequired, Forbidden, TooManyRequests
from app.utils.jwt import verify_token
from app.services.auth_service import check_role

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()


def authentication(request: Request) -> dict:
    token = request.cookies.get("access_token")
    if not token:
        raise AuthRequired()

    payload = verify_token(token)
    return payload


def get_current_user_id(payload: dict = Depends(authentication)) -> int:
    return int(payload["sub"])

def authorized(roles: Iterable[str]) -> Callable[..., Coroutine[Any, Any, None]]:
    allowed = set(roles)

    async def dependency(
        user_id: int = Depends(get_current_user_id),
        db: AsyncSession = Depends(get_db),
    ) -> None:
        role = await check_role(db, user_id)
        if role not in allowed:
            raise Forbidden()

    return dependency


def rate_limit(name: str, max_requests: int, window_seconds: int) -> Callable[[Request], None]:
    def dependency(request: Request) -> None:
        client_ip = request.client.host if request.client else "unknown"
        key = f"{name}:{client_ip}"

        if is_rate_limited(key, max_requests, window_seconds):
            raise TooManyRequests()

    return dependency