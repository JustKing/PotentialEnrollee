from datetime import date

import vk
from flask import Flask, render_template, request, redirect, url_for

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


    @app.route('/potential')
    def potential():
        return render_template("entrants/potential.html", title='Направления')


    @app.route('/find')
    def find(abiturs=None,params=None):
        sort={
            0: 'По популярности',
            1: 'По дате регистрации'
        }
        if abiturs is None:
            return render_template("entrants/find/find.html", title='Поиск', sort=sort, abiturs=1, params=1, today=date.today())
        else:
            if params is None:
                return render_template("entrants/find/find.html", title='Поиск', sort=sort, abiturs=abiturs, params=1, today=date.today())
            else:
                return render_template("entrants/find/find.html", title='Поиск', sort=sort, abiturs=abiturs, params=params, today=date.today())



    @app.route('/find', methods=['POST'])
    def findPost():
        params = {
            'sort': int(request.form['sort']),
            'count': int(request.form['count'])+1,
            'age_from': request.form['age_from'],
            'age_to': request.form['age_to'],
            'city': request.form['city']
        }
        session = vk.Session(access_token='069f2eb61cd727f589778c1a47b891e032a15f66f3c4deb7cfae817e5179325617fc6a2ce94668557c1dc')
        api = vk.API(session, v='5.80', lang='ru')
        abiturs = api.users.search(fields='photo_max_orig, can_write_private_message, bdate', count=params['count'],sort=params['sort'],city=params['city'],age_from=params['age_from'], age_to=params['age_to'])
        for (key, abitur) in abiturs.items():
            if (key == 'items'):
                for abit in abitur:
                    try:
                        abit['bdate']
                    except KeyError:
                        abit['age'] = 'Не указано'
                    else:
                        age=abit['bdate'].replace('.',' ').split()
                        try:
                            age[2]
                        except IndexError:
                            abit['age'] = 'Не указано'
                        else:
                            year=date.today().year-int(age[2])
                            month=date.today().month-int(age[1])
                            day=date.today().day-int(age[0])
                            if(day<=0 and month>=-1):
                                month+=1
                            if((day == 0 and month == 0) or month > 0):
                                year=year
                            else:
                                year-=1
                            abit['age']=year
        return find(abiturs,params)

    return app
