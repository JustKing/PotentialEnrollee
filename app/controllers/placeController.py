from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
)

from sqlalchemy.exc import SQLAlchemyError

from app.models.place import db, Place

module = Blueprint('place', __name__)


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


def getPlaces():
    place = None
    try:
        place = db.session. \
            query(Place.id, Place.id_city)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)

    return place.all()