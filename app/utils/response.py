# app/utils/response.py

from fastapi import status

def success_response(message: str, data=None, status_code=status.HTTP_200_OK):
    if data is None:
        data = {}
    return {
        "status": status_code,
        "message": message,
        "data": data,
    }