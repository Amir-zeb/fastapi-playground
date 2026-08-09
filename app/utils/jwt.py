import jwt
from datetime import datetime, timedelta, UTC
from jwt import ExpiredSignatureError, InvalidTokenError as JWTInvalidTokenError , InvalidSignatureError
from app.exceptions import TokenExpiredError, InvalidTokenError

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        return payload

    except ExpiredSignatureError:
        raise TokenExpiredError()

    except InvalidSignatureError:
        raise InvalidTokenError()

    except JWTInvalidTokenError:
        raise InvalidTokenError()