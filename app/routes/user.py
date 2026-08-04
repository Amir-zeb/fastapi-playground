from fastapi import status, APIRouter,HTTPException,Depends
from app.schema.user import User,UserCreate,UserUpdate,UserDelete
from sqlalchemy.orm import Session
from app.schema.api_response import ApiResponse
from app.services.user_service import get_all_users,get_user_by_id,create_user,update_user,delete_user_by_id
from app.dependencies import get_db
from app.utils.response import success_response

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/all", summary="User Endpoint", description="Returns user information.",response_model=ApiResponse[list[User]])
def get_user_all_endpoint(db:Session=Depends(get_db)):
    users = get_all_users(db)
    return success_response("User information retrieved successfully", users)

@router.get("/{user_id}", summary="Get User by ID", description="Returns information for a specific user.",response_model=ApiResponse[User])
def get_user_by_id_endpoint(user_id: int, db:Session=Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return success_response("User found", user, status_code=status.HTTP_200_OK)

@router.post(
    "/",
    summary="Create User Endpoint",
    description="Creates a new user and adds it to the user list.",
    status_code=status.HTTP_201_CREATED,
    response_model=ApiResponse[UserCreate]
)
def create_user_endpoint(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    return success_response("User created successfully", db_user, status_code=status.HTTP_201_CREATED)

@router.put(
    "/{user_id}",
    summary="Update User Endpoint",
    description="Updates an existing user's information.",
    response_model=ApiResponse[UserUpdate]
)
def update_user_endpoint(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    db_user = update_user(db, user_id, user)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return success_response("User updated successfully", db_user)

@router.delete(
    "/{user_id}",
    summary="Delete User Endpoint",
    description="Deletes an existing user.",
    response_model=ApiResponse[UserDelete]
)
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    db_user = delete_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return success_response("User deleted successfully", {"user_id":user_id})
