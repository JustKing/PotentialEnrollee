from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
    redirect, request, url_for)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.abitur_inf import db, Abitur_inf

module = Blueprint('abitur_inf', __name__)


def log_error(*args, **kwargs):
    current_app.logger.error(*args, **kwargs)


def getInf():
    abitur_inf = None
    try:
        abitur_inf = db.session. \
            query(Abitur_inf)
    except SQLAlchemyError as e:
        log_error('Error while querying database', exc_info=e)
        flash('There was error while querying database', 'danger')
        abort(500)
    return abitur_inf.all()

@module.route('/technical', methods=['POST'])
def saveInf():
    abitur_inf = getInf()
    for abitur in abitur_inf:
        print(abitur)
        if abitur.id_abitur == request.form['idAbitur']:
            abitur_inf['id_status']=int(request.form['status'])
            try:
                db.session.add(abitur_inf)
                try:
                    db.session.commit()
                except IntegrityError as e:
                    return redirect(url_for('abitur.view_tec'))
            except SQLAlchemyError as e:
                log_error('Error while querying database', exc_info=e)
                flash('There was error while querying database', 'danger')
                abort(500)
    return redirect(url_for('abitur.view_tec'))