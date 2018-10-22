from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
)

from sqlalchemy.exc import SQLAlchemyError

from app.models.abitur import db, Abitur

module = Blueprint('abitur', __name__)

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

#составляем массив городов
def arCity(side):
    city = None
    try:
        city = db.session. \
            query(Abitur.city_id, Abitur.city). \
            distinct(Abitur.city). \
            filter(Abitur.id_side == side)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    return city

#составляем массив абитуриентов
def arAbitur(side):
    abitur = None
    try:
        abitur = db.session. \
            query(Abitur). \
            filter(Abitur.id_side == side)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    return abitur

@module.route('/humanities', methods=['GET'])
def view_hum():
    abitur = arAbitur(1)
    city = arCity(1)
    return render_template('entrants/humanities.html', abiturs=abitur, cities=city)

@module.route('/technical', methods=['GET'])
def view_tec():
    abitur = arAbitur(2)
    city = arCity(2)
    return render_template('entrants/technical.html', abiturs=abitur, cities=city)

@module.route('/natural', methods=['GET'])
def view_nat():
    abitur = arAbitur(3)
    city = arCity(3)

    return render_template('entrants/natural.html', abiturs=abitur, cities=city)