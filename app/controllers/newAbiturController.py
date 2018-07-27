from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
    redirect, url_for)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.area import Area
from app.models.newAbitur import db, newAbitur

module = Blueprint('newabitur', __name__)


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


def saveAbitur(abiturient):
    abitur = newAbitur(id=abiturient['id'],
                           first_name = abiturient['first_name'],
                           last_name = abiturient['last_name'],
                           middle_name = abiturient['nickname'])

    try:
        db.session.add(abitur)
        try:
            db.session.commit()
        except IntegrityError as e:
            return redirect(url_for('find'))
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)


def getAbitur():
    abiturs = None
    try:
        abiturs = db.session. \
            query(newAbitur.id, newAbitur.first_name)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    return abiturs.all()

def deleteAbitur():

    return 1