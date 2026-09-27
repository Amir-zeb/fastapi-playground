from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import UserModel
from app.schema.auth import RegisterData
from app.exceptions import EmailAlreadyExistsError, InvalidCredentialsError, UserNotFound
from app.utils.password import hash_password, verify_password
from app.utils.jwt import create_access_token
from app.services.user_service import get_user_be_email

async def login(db: AsyncSession, email: str, password: str) -> tuple[UserModel, str]:
    result = await db.execute(select(UserModel).filter(UserModel.email == email))
    user = result.scalar_one_or_none()

    if user and verify_password(password, user.password):
        token = create_access_token(user.id)
        return user, token

    raise InvalidCredentialsError()


async def register(db: AsyncSession, data: RegisterData) -> UserModel:
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


async def get_user(db: AsyncSession, payload: dict) -> UserModel:
    user_id = int(payload["sub"])
    user = await get_user_by_id(db, user_id)
    if not user:
        raise UserNotFound()
    return user


async def get_user_by_id(db: AsyncSession, user_id: int) -> UserModel | None:
    result = await db.execute(select(UserModel).filter(UserModel.id == user_id))
    return result.scalar_one_or_none()


async def check_role(db: AsyncSession, user_id: int) -> str | None:
    result = await db.execute(select(UserModel.role).filter(UserModel.id == user_id))
    row = result.first()
    return row[0] if row else None