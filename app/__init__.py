from flask import Flask, render_template

from app.database import db


def create_app():

    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/ssomo'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    app.config.update(dict(
        DATABASE=db,
        DEBUG=False,
        SECRET_KEY='o4en s1ojn!y k1u4!k d1ya vz1oma#',
        USERNAME='postgres',
        PASSWORD='admin'
    ))

    import app.controllers.abitur as abitur
    #передаем управление маршрутами соответсвующему контроллеру
    app.register_blueprint(abitur.module)

    #route-маршруты
    @app.route('/')
    def index():
        return render_template("index.html", title='Потенциальные абитуриенты')

    #потом перенести так же как и первый
    @app.route('/potential')
    def potential():
        return render_template("entrants/potential.html", title='Направления')


    return app
