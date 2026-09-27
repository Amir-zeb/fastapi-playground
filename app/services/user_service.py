from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserModel
from app.schema.user import UserUpdate, UserCreate, User
from app.exceptions import UserNotFound, EmailAlreadyExistsError
from app.utils.password import hash_password


async def create_user(db: AsyncSession, data: UserCreate) -> UserModel:
    user_found = await get_user_be_email(db, data.email)
    if user_found:
        raise EmailAlreadyExistsError()

    user_data = data.model_dump()
    user_data["password"] = hash_password(data.password)

    db_user = UserModel(**user_data)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


# OLD pattern: returns raw ORM instances — relies entirely on response_model to filter password
# async def get_all_users(db: AsyncSession) -> list[UserModel]:
#     result = await db.execute(select(UserModel))
#     return list(result.scalars().all())

# NEW pattern: filters/validates at the service boundary — password never leaves this function
async def get_all_users(db: AsyncSession) -> list[User]:
    result = await db.execute(select(UserModel))
    users = result.scalars().all()
    return [User.model_validate(u) for u in users]


async def get_user_by_id(db: AsyncSession, user_id: int) -> UserModel:
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise UserNotFound()
    return user


async def update_user(db: AsyncSession, user_id: int, user_data: UserUpdate) -> UserModel:
    user = await get_user_by_id(db, user_id)

    update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
    if "password" in update_data:
        update_data["password"] = hash_password(update_data["password"])
    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user


async def delete_user_by_id(db: AsyncSession, user_id: int) -> None:
    db_user = await get_user_by_id(db, user_id)

    await db.delete(db_user)
    await db.commit()


async def get_user_be_email(db: AsyncSession, email: str) -> UserModel | None:
    result = await db.execute(select(UserModel).filter(UserModel.email == email))
    return result.scalar_one_or_none()