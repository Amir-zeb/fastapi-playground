from pydantic import BaseModel, Field, EmailStr
from app.schema.user import Gender, UserBase

class LoginCredentials(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=16)
    
class RegisterData(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=1, max_length=16)
    age: int = Field(..., gt=0)
    gender : Gender = Field(..., description="Gender of the user, must be either 'male' or 'female'")

class AuthenticatedUser(UserBase):
    id: int

class LoginResponse(AuthenticatedUser):
    pass

class RegisterResponse(BaseModel):
    pass