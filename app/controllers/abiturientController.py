from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
    redirect, url_for)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.abiturient import db, abiturient

module = Blueprint('abiturient', __name__)


def saveAbitur(abit):
    abitur = abiturient(id=abit['id'],
                           firstName = abit['first_name'],
                           lastName = abit['last_name'],
                           middleName = abit['nickname'])
    try:
        db.session.add(abitur)
        try:
            db.session.commit()
        except IntegrityError as e:
            return redirect(url_for('find'))
    except SQLAlchemyError as e:
        flash('There was error while querying database', 'danger')
        return redirect(url_for('find'))


def getAbitur():
    abiturs = None
    try:
        abiturs = db.session. \
            query(abiturient.id, abiturient.firstName)
    except SQLAlchemyError as e:
        flash('There was error while querying database', 'danger')
        abort(500)
    return abiturs.all()
