from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
)

from sqlalchemy.exc import SQLAlchemyError

from app.models.area import db, Area
from app.models.city import City

module = Blueprint('area', __name__)


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


def getAreasWithCities():
    areaWithCities = None
    result = None
    try:
        areaWithCities = db.session.\
            query(Area.title, City.id).\
            join(City, City.idArea == Area.id)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    areas = {}
    nij, sov, kon, oct, ber, bel, nef, sur, kha = 'Нижневартовский район', 'Советский район', 'Кондинский район', 'Октябрьский район', 'Березовский район', 'Белоярский район', 'Нефтеюганский район', 'Сургутский район', 'Ханты-Мансийский район'
    areas[nij] = list()
    areas[sov] = list()
    areas[kon] = list()
    areas[oct] = list()
    areas[ber] = list()
    areas[bel] = list()
    areas[nef] = list()
    areas[sur] = list()
    areas[kha] = list()
    for (key,city) in areaWithCities.all():
        while switch(key):
            if case('Нижневартовский район'):
                areas[nij].append(city)
                break
            if case('Советский район'):
                areas[sov].append(city)
                break
            if case('Кондинский район'):
                areas[kon].append(city)
                break
            if case('Октябрьский район'):
                areas[oct].append(city)
                break
            if case('Березовский район'):
                areas[ber].append(city)
                break
            if case('Белоярский район'):
                areas[bel].append(city)
                break
            if case('Нефтеюганский район'):
                areas[nef].append(city)
                break
            if case('Сургутский район'):
                areas[sur].append(city)
                break
            if case('Ханты-Мансийский район'):
                areas[kha].append(city)
                break
    return areas


def getAreas():
    area = None
    try:
        area = db.session.\
            query(Area.title)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)

    return area.all()

class switch(object):
    value = None
    def __new__(class_, value):
        class_.value = value
        return True

def case(*args):
    return any((arg == switch.value for arg in args))