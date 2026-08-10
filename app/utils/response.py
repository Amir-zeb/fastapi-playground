# app/utils/response.py

from fastapi import status
from typing import Any

def success_response(message: str, data:Any=None, status_code:int=status.HTTP_200_OK) -> dict[str, Any]:
    if data is None:
        data = {}
    return {
        "status": status_code,
        "message": message,
        "data": data,
    }