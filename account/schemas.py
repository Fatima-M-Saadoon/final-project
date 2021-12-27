from typing import Optional

from ninja import Schema
from pydantic import EmailStr, Field, UUID4


class AccountCreate(Schema):
    name: str

    phone_number: str
    address1: str
    username: str
    # email: EmailStr
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)


class AccountOut(Schema):
    id: UUID4
    name: str
    phone_number: str
    address1: str
    username: str



class TokenOut(Schema):
    access: str


class AuthOut(Schema):
    token: TokenOut
    account: AccountOut


class SigninSchema(Schema):
    username: str
    password: str


class AccountUpdate(Schema):
    name: str
    username: str
    phone_number: Optional[str]
    address1: str


class ChangePasswordSchema(Schema):
    old_password: str
    new_password1: str
    new_password2: str
