from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
)

from sqlalchemy.exc import SQLAlchemyError

from app.models.abitur import db, Abitur
import app.controllers.statusController as st

module = Blueprint('abitur', __name__)

def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)

@module.route('/humanities', methods=['GET'])
def view_hum():
    status = st.getStatus()
    abitur = None
    try:
        abitur = db.session.\
            query(Abitur).\
            filter(Abitur.id_side == 1)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    city = None
    try:
        city = db.session. \
            query(Abitur.city_id, Abitur.city). \
            distinct(Abitur.city_id). \
            filter(Abitur.id_side == 1)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    return render_template('entrants/humanities.html', abiturs=abitur, cities=city, status=status)

@module.route('/technical', methods=['GET'])
def view_tec():
    status = st.getStatus()
    abitur = None
    try:
        abitur = db.session.\
            query(Abitur).\
            filter(Abitur.id_side == 2)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    city = None
    try:
        city = db.session.\
            query(Abitur.city_id, Abitur.city).\
            distinct(Abitur.city_id).\
            filter(Abitur.id_side == 2)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    return render_template('entrants/technical.html', abiturs=abitur, cities=city, status=status)

@module.route('/natural', methods=['GET'])
def view_nat():
    status = st.getStatus()
    abitur = None
    try:
        abitur = db.session.\
            query(Abitur).\
            filter(Abitur.id_side == 3)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    city = None
    try:
        city = db.session. \
            query(Abitur.city_id, Abitur.city). \
            distinct(Abitur.city_id). \
            filter(Abitur.id_side == 3)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    return render_template('entrants/natural.html', abiturs=abitur, cities=city, status=status)

@module.route('/delete')
def del_abitur():
    return render_template("entrants/danger/deleteAbitur.html", title='Удаление абитуриента')