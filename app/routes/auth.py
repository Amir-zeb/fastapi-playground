from fastapi import APIRouter, Depends, Response, status
from app.dependencies import get_db
from app.schema.auth import LoginCredentials, RegisterData, RegisterResponse, LoginResponse
from app.services.auth_service import login, register
from app.utils.response import success_response
from app.schema.api_response import ApiResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/login",
    summary="Login Endpoint",
    description="Handles user login.",
    response_model=ApiResponse[LoginResponse],
    responses={
        200: {
            "description": "Successful login",
            "headers": {
                "set-cookie": {
                    "description": "HttpOnly authentication cookie",
                    "schema": {"type": "string"},
                }
            },
        }
    },
)
def login_endpoint(credentials: LoginCredentials, response: Response, db=Depends(get_db)):
    user, token = login(db, credentials.email, credentials.password)

    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,  # True in production (HTTPS)
        samesite="lax",
        max_age=3600,
    )
    
    return success_response(
        "user logged in successfully",
        user,
    )

@router.post(
    "/register",
    summary="Register Endpoint",
    description="Handles user registration.",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[RegisterResponse],
)
def register_endpoint(register_data: RegisterData, db=Depends(get_db)):
    register(db, register_data)
    return success_response(
        "user registered successfully",
        status_code=status.HTTP_201_CREATED,
    )

@router.post("/logout", summary="Logout Endpoint", description="Handles user logout.")
def logout():   
    return {"message": "Logout endpoint"}

@router.get("/me", summary="User Information Endpoint", description="Retrieves authenticated user information.")
def me():
    return {"message": "Authenticated user information"}