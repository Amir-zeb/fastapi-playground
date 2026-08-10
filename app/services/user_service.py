from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schema.user import UserUpdate, UserCreate, User
from app.exceptions import UserNotFound, EmailAlreadyExistsError
from app.utils.password import hash_password

def create_user(db: Session, data: UserCreate)->UserModel:
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

# OLD pattern: returns raw ORM instances — relies entirely on response_model to filter password
# def get_all_users(db: Session) -> list[UserModel]:
#     return db.query(UserModel).all()

# NEW pattern: filters/validates at the service boundary — password never leaves this function
def get_all_users(db: Session) -> list[User]:
    users = db.query(UserModel).all()
    return [User.model_validate(u) for u in users]

def get_user_by_id(db: Session, user_id: int) -> UserModel:
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise UserNotFound()
    return user

def update_user(db: Session, user_id: int, user_data: UserUpdate)->UserModel:
    user = get_user_by_id(db, user_id)

    update_data = user_data.model_dump(exclude_unset=True,exclude_none=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)

    return user

def delete_user_by_id(db: Session, user_id: int)->None:
    db_user = get_user_by_id(db, user_id)

    db.delete(db_user)
    db.commit()

def get_user_be_email(db: Session, email: str)->UserModel|None:
    return db.query(UserModel).filter(UserModel.email == email).first()
