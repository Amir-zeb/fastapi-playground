from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schema.auth import RegisterData
from app.exceptions import EmailAlreadyExistsError, InvalidCredentialsError

def login(db: Session, email: str, password: str):
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if user and user.password == password:
        return user
    else:
        raise InvalidCredentialsError()

def register(db: Session, data:RegisterData):
    is_exists = existing_user(db, data.email)
    if is_exists:
        raise EmailAlreadyExistsError()
    
    db_user = UserModel(**data.model_dump())
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def existing_user(db: Session, email: str):
    return db.query(UserModel).filter(UserModel.email == email).first()