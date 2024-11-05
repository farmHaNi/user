
from datetime import datetime
from pydantic import EmailStr
from sqlmodel import Field, SQLModel

from app.enums.user_type import UserType


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(unique=True)
    name: str
    password: str
    email: EmailStr
    type: UserType
    create_date: datetime = Field(default_factory=datetime.now)
