from flask import Blueprint, request, current_app
from sqlalchemy import func

from .model import Grid
from config import const

api = Blueprint('api', __name__)


@api.route('/populationInsights')
def get_data():
    lng = request.args.get('lng')
    lat = request.args.get('lat')
    grid = Grid.query.filter(func.ST_Contains(
        Grid.box, 'SRID={};POINT({} {})'.format(const.get('SRID'), lng, lat))).first()
    print(grid.city, grid.grid_id)
    return 'hello'
