from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
    redirect, url_for)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.status import db, Status

module = Blueprint('status', __name__)


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


def getStatus():
    status = None
    try:
        status = db.session. \
            query(Status.id, Status.name).order_by(Status.id.asc())
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)

    return status.all()

def saveStatus(status):
    stat = Status(name = status)
    try:
        db.session.add(stat)
        try:
            db.session.commit()
        except IntegrityError as e:
            return redirect(url_for('status'))
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)