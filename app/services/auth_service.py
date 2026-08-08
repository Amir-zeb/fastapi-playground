from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schema.auth import RegisterData
from app.exceptions import EmailAlreadyExistsError, InvalidCredentialsError
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token

def login(db: Session, email: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user and verify_password(password, user.password):
        token = create_access_token(user.id)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "age": user.age,
            "gender": user.gender,
        }, token
        # return user, token

    raise InvalidCredentialsError()

def register(db: Session, data:RegisterData):
    is_exists = existing_user(db, data.email)
    if is_exists:
        raise EmailAlreadyExistsError()
    
    user_data = data.model_dump()
    user_data["password"] = hash_password(data.password)

    db_user = UserModel(**user_data)
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def existing_user(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()