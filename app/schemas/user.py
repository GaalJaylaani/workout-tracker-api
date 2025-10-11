from pydantic import BaseModel, EmailStr, constr,  ConfigDict



PasswordStr = constr(min_length=6, max_length=256)

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
