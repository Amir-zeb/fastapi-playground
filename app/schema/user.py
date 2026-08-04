from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field

class Gender(str, Enum):
    MALE = "male"
    FEMALE = "female"


class UserBase(BaseModel):
    name: str
    email: str
    age: int
    gender: Gender
    
class User(UserBase):
    id: int

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    email: Optional[str] = Field(None, min_length=1)
    age: Optional[int] = Field(None, gt=0)
    gender: Optional[Gender] = None

class UserDelete(BaseModel):
    user_id: int