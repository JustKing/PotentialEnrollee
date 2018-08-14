import time

import vk

from flask import Flask, render_template, request, redirect, url_for
from datetime import date

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

    # передаем управление маршрутами соответсвующему контроллеру
    import app.controllers.abiturController as abitur
    import app.controllers.abitur_infController as abiturInf
    import app.controllers.newAbiturController as newabitur
    import app.controllers.areaController as ar
    import app.controllers.statusController as st
    app.register_blueprint(abitur.module)
    app.register_blueprint(abiturInf.module)
    app.register_blueprint(ar.module)
    app.register_blueprint(newabitur.module)
    app.register_blueprint(st.module)

    # route-маршруты
    @app.route('/')
    def index():
        return render_template("index.html", title='Потенциальные абитуриенты')

    @app.route('/potential')
    def potential():
        status = st.getStatus()
        return render_template("entrants/potential.html", title='Направления')

    @app.route('/danger')
    def danger():
        return render_template("entrants/danger/dangerZone.html", title='Опасность')

    @app.route('/status')
    def status():
        status = st.getStatus()
        return render_template("entrants/danger/editStatus.html", title='Редактирование статуса', status=status)

    @app.route('/status', methods=['POST'])
    def saveStatus():
        st.saveStatus(request.form['name'])
        return status()

    @app.route('/saveInf', methods=['POST'])
    def saveInf():
        abiturInf.saveInf(request.form['idAbitur'], request.form['status']);
        return redirect(url_for('abitur.view_tec'))

    @app.route('/find')
    def find(abiturs=None, params=None):
        sort = {
            0: 'По популярности',
            1: 'По дате регистрации'
        }

        areas = ar.getAreasWithCities()
        if abiturs is None:
            return render_template("entrants/find/find.html", title='Поиск', sort=sort, abiturs=1, params=1,
                                   areas=areas)
        else:
            if params is None:
                return render_template("entrants/find/find.html", title='Поиск', sort=sort, abiturs=abiturs, params=1,
                                       areas=areas)
            else:
                return render_template("entrants/find/find.html", title='Поиск', sort=sort, abiturs=abiturs,
                                       params=params, areas=areas)

    @app.route('/find', methods=['POST'])
    def findUsers():
        params = {
            'sort': int(request.form['sort']),
            'count': int(request.form['count']),
            'age_from': request.form['age_from'],
            'age_to': request.form['age_to'],
            'area': request.form['area']
        }
        inDbAbiturs = newabitur.getAbitur()
        session = vk.Session(
            access_token='069f2eb61cd727f589778c1a47b891e032a15f66f3c4deb7cfae817e5179325617fc6a2ce94668557c1dc')
        api = vk.API(session, v='5.80', lang='ru')
        params['area'] = params['area'][1:-1]
        params['area'] = params['area'].split(', ')
        abits = []
        c = 0
        countFind = len(params['area'])*params['count']
        count = params['count'] - 1
        id = 0
        while countFind>0:
            print(countFind)
            count+=1
            for city in params['area']:
                if c < 3:
                    c += 1
                else:
                    time.sleep(1)
                    c = 1
                    print('sleep')
                abiturs = api.users.search(fields='nickname, photo_max_orig, can_write_private_message, bdate',
                                           count=count, sort=params['sort'], city=city,
                                           age_from=params['age_from'], age_to=params['age_to'])
                for inDb in inDbAbiturs:
                    for (key, abitur) in abiturs.items():
                        if (key == 'items'):
                            for abit in abitur:
                                if inDb[0] == abit['id']:
                                    abit['inDb']=1
                print(abiturs)
                for (key, abitur) in abiturs.items():
                    if (key == 'items'):
                        for abit in abitur:
                            if id != abit['id']:
                                if 'inDb' in abit:
                                    ''
                                else:
                                    try:
                                        abit['bdate']
                                    except KeyError:
                                        abit['age'] = 'Не указано'
                                    else:
                                        age = abit['bdate'].replace('.', ' ').split()
                                        try:
                                            age[2]
                                        except IndexError:
                                            abit['age'] = 'Не указано'
                                        else:
                                            year = date.today().year - int(age[2])
                                            month = date.today().month - int(age[1])
                                            day = date.today().day - int(age[0])
                                            if (day <= 0 and month >= -1):
                                                month += 1
                                            if ((day == 0 and month == 0) or month > 0):
                                                year = year
                                            else:
                                                year -= 1
                                            abit['age'] = year
                                    abits.append(abit)
                                    onSave = abit
                                    id=abit['id']
                                    newabitur.saveAbitur(onSave)
                                    countFind -= len(abits)
        return find(abits, params)

    return app
