from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
)

from sqlalchemy.exc import SQLAlchemyError

from app.models.enrollee import db, Enrollee

module = Blueprint('enrollee', __name__)


# составляем массив городов
def arCity(side):
    city = None
    try:
        city = db.session. \
            query(Enrollee.idCity, Enrollee.city). \
            distinct(Enrollee.city). \
            filter(Enrollee.idSide == side)
    except SQLAlchemyError as e:
        flash('There was error while querying database', 'danger')
        abort(500)
    return city


# составляем массив абитуриентов
def arEnrollee(side):
    abitur = None
    try:
        abitur = db.session. \
            query(Enrollee). \
            filter(Enrollee.idSide == side)
    except SQLAlchemyError as e:
        flash('There was error while querying database', 'danger')
        abort(500)
    return abitur


@module.route('/humanities', methods=['GET'])
def view_hum():
    enrollee = arEnrollee(1)
    city = arCity(1)
    return render_template('entrants/humanities.html', enrolles=enrollee, cities=city)


@module.route('/technical', methods=['GET'])
def view_tec():
    enrollee = arEnrollee(2)
    city = arCity(2)
    return render_template('entrants/technical.html', enrolles=enrollee, cities=city)


@module.route('/natural', methods=['GET'])
def view_nat():
    enrollee = arEnrollee(3)
    city = arCity(3)

    return render_template('entrants/natural.html', enrolles=enrollee, cities=city)
