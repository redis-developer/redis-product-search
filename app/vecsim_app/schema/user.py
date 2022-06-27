import typing as t
from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str = None
    permissions: str = "user"

class UserBase(BaseModel):
    email: str
    is_active: bool = True
    is_superuser: bool = False
    first_name: str = None
    last_name: str = None
    title: str = None
    company: str = None

class UserOut(UserBase):
    pass

class UserCreate(UserBase):
    password: str

class UserEdit(UserBase):
    password: t.Optional[str] = None

class UserSchema(UserBase):
    pk: str
    id: int