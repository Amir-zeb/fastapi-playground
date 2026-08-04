from sqlalchemy.orm import Session
from app.models.user import UserModel
from app.schema.user import User, UserUpdate

def get_all_users(db: Session):
    return db.query(UserModel).all()

def get_user_by_id(db: Session, user_id: int):
    return db.query(UserModel).filter(UserModel.id == user_id).first()

def create_user(db: Session, user: User):
    db_user = UserModel(**user.model_dump())
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def update_user(db: Session, user_id: int, user: UserUpdate):
    db_user = get_user_by_id(db, user_id)

    if not db_user:
        return None

    update_data = user.model_dump(exclude_unset=True,exclude_none=True)

    for key, value in update_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)

    return db_user

def delete_user_by_id(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id)
    
    if not db_user:
        return None
    
    db.delete(db_user)
    db.commit()
    
    return user_id