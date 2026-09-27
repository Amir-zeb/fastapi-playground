from fastapi import status, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.schema.user import User, UserUpdate, UserUpdateResponse, UserCreateResponse, UserDeleteResponse, UserCreate
from app.schema.api_response import ApiResponse
from app.services.user_service import create_user, get_all_users, get_user_by_id, update_user, delete_user_by_id
from app.dependencies import get_db, authentication, authorized
from app.utils.response import success_response

router = APIRouter(prefix="/user", tags=["User"], dependencies=[Depends(authentication), Depends(authorized({"admin"}))])

@router.post(
    "/create",
    summary="Create User Endpoint",
    description="Creates a new user and adds it to the user list.",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[UserCreateResponse]
)
async def create_user_endpoint(user_data: UserCreate, db: AsyncSession = Depends(get_db)) -> dict:
    db_user = await create_user(db, user_data)
    return success_response("User created successfully", db_user, status_code=status.HTTP_201_CREATED)

@router.get("/all", summary="User Endpoint", description="Returns user information.", response_model=ApiResponse[list[User]])
async def get_user_all_endpoint(db: AsyncSession = Depends(get_db)) -> dict:
    users = await get_all_users(db)
    return success_response("User information retrieved successfully", users)

@router.get("/{user_id}", summary="Get User by ID", description="Returns information for a specific user.", response_model=ApiResponse[User])
async def get_user_by_id_endpoint(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    user = await get_user_by_id(db, user_id)
    return success_response("User found", user, status_code=status.HTTP_200_OK)

@router.put(
    "/{user_id}",
    summary="Update User Endpoint",
    description="Updates an existing user's information.",
    response_model=ApiResponse[UserUpdateResponse]
)
async def update_user_endpoint(user_id: int, user_data: UserUpdate, db: AsyncSession = Depends(get_db)) -> dict:
    updated_user = await update_user(db, user_id, user_data)
    return success_response("User updated successfully", updated_user)

@router.delete(
    "/{user_id}",
    summary="Delete User Endpoint",
    description="Deletes an existing user.",
    response_model=ApiResponse[UserDeleteResponse]
)
async def delete_user_endpoint(user_id: int, db: AsyncSession = Depends(get_db)) -> dict:
    await delete_user_by_id(db, user_id)
    return success_response("User deleted successfully", {"user_id": user_id})