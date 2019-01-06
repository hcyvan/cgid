from sqlalchemy import Column, String

from .base import BaseModel


class User(BaseModel):
    id = Column(String(128), primary_key=True)
    password = Column(String(64))
