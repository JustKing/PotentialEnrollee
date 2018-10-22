from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
    redirect, request, url_for)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.enrolleeInformation import db, enrolleeInformation

module = Blueprint('abitur_inf', __name__)

def getInf():
    abitur_inf = None
    try:
        abitur_inf = db.session. \
            query(enrolleeInformation)
    except SQLAlchemyError as e:
        flash('There was error while querying database', 'danger')
        abort(500)
    return abitur_inf.all()

@module.route('/technical', methods=['POST'])
def saveInf():
    enrolleeInformation = getInf()
    for abitur in enrolleeInformation:
        print(abitur)
        if abitur.id_abitur == request.form['idAbitur']:
            enrolleeInformation['id_status']=int(request.form['status'])
            try:
                db.session.add(enrolleeInformation)
                try:
                    db.session.commit()
                except IntegrityError as e:
                    return redirect(url_for('abitur.view_tec'))
            except SQLAlchemyError as e:
                flash('There was error while querying database', 'danger')
                abort(500)
    return redirect(url_for('abitur.view_tec'))