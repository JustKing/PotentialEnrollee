from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
)

from sqlalchemy.exc import SQLAlchemyError

from app.models.city import db, City

module = Blueprint('city', __name__)


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


def getCities():
    city = None
    try:
        city = db.session. \
            query(City.id, City.title)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)

    return city.all()