from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from app.routes.user import router as user_router
from app.models.user import Base
from app.database import engine

Base.metadata.create_all(bind=engine)

app=FastAPI(title="FastAPI Playground", description="This is a simple FastAPI application.", version="1.0.0")

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException,
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": exc.status_code,
            "message": exc.detail,
            "data": None,
        },
    )

app.include_router(user_router)

@app.get("/health", tags=["Health Check"], summary="Health Check Endpoint", description="Returns a simple message indicating that the application is running.")
def root():
    return {"message": "Hello, World!"}
