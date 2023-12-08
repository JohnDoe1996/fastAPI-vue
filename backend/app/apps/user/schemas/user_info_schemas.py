from typing import Union, List
from pydantic import BaseModel, AnyHttpUrl, conint


class LoginUserInfoSchema(BaseModel):
    user: str
    password: str
    code: str = ""
    key: str = ""


class RegisterUserInfoSchema(BaseModel):
    username: str
    email: str
    phone: str
    password: str
    sex: int = 0
    nickname: str = ""
    avatar: str = ""
    code: str = ""
    key: str = ""


class ForgetPasswordSubmitSchema(BaseModel):
    email: str
    code: str = ""
    key: str = ""


class ForgetPasswordSetPasswordSchema(BaseModel):
    password: str
    code: str = ""
    key: str = ""


class ChangeUserInfoSchema(BaseModel):
    nickname: str
    email: str
    phone: str
    sex: str


class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str


class UserAvailabilitySchema(BaseModel):
    data: str
    exclude_user_id: int = None
