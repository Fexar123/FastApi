from pydantic import BaseModel, EmailStr
from modules.Role import Role
from abc import ABC

class abc_UserSchema(ABC, BaseModel):
    pass

class UserSchema(abc_UserSchema):
    username: str
    email: EmailStr
    password: str
    role: str = Role.basic


class UserSchemaPrem(UserSchema):
    role:str = Role.premium


class UserResponse(UserSchema):
    id: int