from sqlalchemy import Column, String, Integer
from geoalchemy2 import Geometry

from .base import BaseModel


class Grid(BaseModel):
    id = Column(Integer, primary_key=True)
    city = Column(String(16))
    grid_id = Column(String(16))
    center = Column(Geometry(geometry_type='POINT'))
    box = Column(Geometry(geometry_type='POLYGON'))
