from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schema.auth import RegisterData
from app.exceptions import EmailAlreadyExistsError, InvalidCredentialsError, UserNotFound
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.services.user_service import get_user_be_email

def login(db: Session, email: str, password: str)-> tuple[UserModel,str]:
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user and verify_password(password, user.password):
        token = create_access_token(user.id)
        return user, token

    raise InvalidCredentialsError()

def register(db: Session, data:RegisterData)->UserModel:
    user_found = get_user_be_email(db, data.email)
    if user_found:
        raise EmailAlreadyExistsError()
    
    user_data = data.model_dump()
    user_data["password"] = hash_password(data.password)

    db_user = UserModel(**user_data)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def get_user(db: Session,payload:dict)->UserModel:
    user_id=int(payload["sub"])
    user= get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound()
    return user

def get_user_by_id(db: Session, user_id: int)-> UserModel|None:
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def check_role(db: Session, user_id: int)-> str | None:
    result = db.query(UserModel.role).filter(UserModel.id == user_id).first()
    return result[0] if result else None