from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import JSONB

from .base import BaseModel


class Detail(BaseModel):
    id = Column(Integer, primary_key=True)
    city = Column(String(16))
    grid_id = Column(String(16))
    week = Column(String(16))

    stay = Column(JSONB)
    insight = Column(JSONB)
    human_traffic = Column(JSONB)
    consumption = Column(JSONB)
    mobile_phone = Column(JSONB)


