import datetime
from typing import Optional

from pydantic import EmailStr, model_validator
from sqlmodel import SQLModel, Field, Relationship


class User(SQLModel, table=True):
    id: Optional[int] = Field(primary_key=True)
    username: str = Field(index=True) # to create database index for fast lookup
    password: str = Field(max_length=256, min_length=6)
    email: EmailStr
    created_at: datetime.datetime = datetime.datetime.now()
    is_seller: bool = False


class UserInput(SQLModel):
    username: str
    password: str = Field(max_length=256, min_length=6)
    password2: str
    email: EmailStr
    is_seller: bool = False

    @model_validator(mode="after")
    def password_match(self):
        if self.password != self.password2:
            raise ValueError("passwords don't match")
        return self


class UserLogin(SQLModel):
    username: str
    password: str