from sqlalchemy import Column, String, Integer
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry

from .base import BaseModel
from config import const


class Grid(BaseModel):
    id = Column(Integer, primary_key=True)
    city = Column(String(16))
    grid_id = Column(String(16))
    box = Column(Geometry(geometry_type='POLYGON', srid=const.get('SRID')))

    stay = Column(JSONB)
    mobile_phone = Column(JSONB)
    consumption = Column(JSONB)
    human_traffic = Column(JSONB)
    insight = Column(JSONB)
