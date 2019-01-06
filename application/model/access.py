from sqlalchemy import Column, String, Integer

from .base import BaseModel


class Access(BaseModel):
    id = Column(Integer, primary_key=True)
    cid = Column(String(128))
    day = Column(String(16))
    count = Column(Integer)
