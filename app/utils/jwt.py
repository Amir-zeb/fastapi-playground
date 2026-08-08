import jwt
from datetime import datetime, timedelta, UTC

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"


def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(UTC) + timedelta(hours=1),
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)