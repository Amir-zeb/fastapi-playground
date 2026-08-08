from fastapi import FastAPI, HTTPException, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.models.user import Base
from app.database import engine
from app.exceptions import AppException

Base.metadata.create_all(bind=engine)

app=FastAPI(title="FastAPI Playground", description="This is a simple FastAPI application.", version="1.0.0")

@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status,
        content={
            "status": exc.status,
            "message": exc.detail,
        },
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "message": "Validation failed",
            "detail": exc.errors(),
        },
    )

@app.exception_handler(Exception)
async def internal_server_error_handler(
    request: Request,
    exc: Exception,
):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "message": "Internal server error",
            "detail": None,
        },
    )

# @app.exception_handler(HTTPException)
# async def http_exception_handler(
#     request: Request,
#     exc: HTTPException,
# ):
#     return JSONResponse(
#         status_code=exc.status_code,
#         content={
#             "status": exc.status_code,
#             "message": exc.detail,
#             "detail": None,
#         },
#     )

app.include_router(auth_router)
app.include_router(user_router)

@app.get("/health", tags=["Health Check"], summary="Health Check Endpoint", description="Returns a simple message indicating that the application is running.")
def root():
    return {"message": "Hello, World!"}
