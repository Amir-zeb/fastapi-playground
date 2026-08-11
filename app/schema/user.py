from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"
    
class RoleEnum(str, Enum):
    USER = "user"
    ADMIN = "admin"


class UserBase(BaseModel):
    model_config = {"from_attributes": True}
    name: str
    email: str
    age: int
    gender: Gender
    role: RoleEnum
    
class User(UserBase):
    id: int

class UserCreateResponse(UserBase):
    id: int
class UserUpdateResponse(UserBase):
    id: int
    
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=16)
    age: int = Field(..., gt=0)
    gender : Gender = Field(..., description="Gender of the user, must be either 'male' or 'female'")

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, gt=0)
    password: Optional[str] = Field(None, gt=0)
    gender: Optional[Gender] = None

class UserDeleteResponse(BaseModel):
    user_id: int