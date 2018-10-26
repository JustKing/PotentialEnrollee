from flask import (
    Blueprint,
    render_template,
    flash,
    abort,
    current_app,
    redirect, url_for)

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from catboost import CatBoostClassifier, Pool
from app.models.abiturient import db, abiturient

import psycopg2

from app.models.city import City

module = Blueprint('abiturient', __name__)


def predictModel(test_data):
    from_file = CatBoostClassifier()
    from_file.load_model("model_catboost", format='cbm')
    predict_data = from_file.predict(test_data, prediction_type='Class')
    print(int(predict_data[0][0]), "- предсказанный класс")
    return predict_data[0][0]


def getTrainModel():
    try:
        conn = psycopg2.connect(dbname='abit', password='admin', user='postgres')
        cur = conn.cursor()
        cur.execute("""
        SELECT i.id_user, i.political, i.alcohol, i.religion, i.smoking, i.life_main, i.people_main, i.sex, i.idFaculty, f.idSide
        FROM public.faculty as f
        JOIN enrolleeInformations as i on i.idFaculty=f.id
        Where f.idSide<4 and (case when political = '' then 0 else 1 end+
            case when alcohol = '' then 0 else 1 end+
            case when people_main = '' then 0 else 1 end+
            case when life_main = '' then 0 else 1 end+
            case when smoking = '' then 0 else 1 end+
            case when religion = '' then 0 else 1 end+
            case when sex is null then 0 else 1 end) > 5
        """)

        id1 = 0
        id2 = 0
        id3 = 0

        train_data = []
        test_data = []
        train_labels = []
        test_labels = []

        response = cur.fetchall()
        lenght = len(response)

        for row in response:
            if int(row[9]) == 1:
                id1 = id1 + 1
            elif int(row[9]) == 2:
                id2 = id2 + 1
            else:
                id3 = id3 + 1

            political = 0
            alcohol = 0
            religion = 0
            smoking = 0
            life_main = 0
            people_main = 0

            if row[1] == '':
                political = 0
            else:
                political = row[1]
            if row[2] == '':
                alcohol = 0
            else:
                alcohol = row[2]
            if row[4] == '':
                smoking = 0
            else:
                smoking = row[4]
            if row[5] == '':
                life_main = 0
            else:
                life_main = row[5]
            if row[6] == '':
                people_main = 0
            else:
                people_main = row[6]

            if row[3] == "":
                religion = 0
            elif row[3] == "Иудаизм":
                religion = 1
            elif row[3] == "Православие":
                religion = 2
            elif row[3] == "Католицизм":
                religion = 3
            elif row[3] == "Протестантизм":
                religion = 4
            elif row[3] == "Ислам":
                religion = 5
            elif row[3] == "Буддизм":
                religion = 6
            elif row[3] == "Конфуцианство":
                religion = 7
            elif row[3] == "Светский гуманизм":
                religion = 8
            elif row[3] == "Пастафарианство":
                religion = 9
            else:
                religion = 10
            train_data.append([int(political), int(alcohol), int(religion), int(smoking), int(life_main), \
                               int(people_main), int(row[7])])
            train_labels.append(int(row[9]))
            test_data.append([int(political), int(alcohol), int(religion), int(smoking), int(life_main), \
                              int(people_main), int(row[7])])
            test_labels.append(int(row[9]))

        # сюда кэтбуст
        lenght_train = int(lenght * 0.85)
        # Данные для обучения
        train_data = train_data[:lenght_train]
        train_labels = train_labels[:lenght_train]
        # Данные для тестирования
        test_data = test_data[lenght_train:]
        test_labels = test_labels[lenght_train:]
        # Уравнивание весов для классов
        maximumid = max(id1, id2, id3)
        weight = [0, maximumid / id1, maximumid / id2, maximumid / id3]
        train_pool = Pool(train_data, train_labels)
        test_pool = Pool(test_data, test_labels)

        model = CatBoostClassifier(iterations=100, verbose=True, loss_function='MultiClass', classes_count=4,
                                   learning_rate=0.01, class_weights=weight, depth=6, eval_metric='Accuracy')
        model.fit(train_pool, eval_set=test_pool)
        model.save_model('model_catboost')
        return True

    except Exception as e:
        print('ERROR: ', e)
        return False


def saveAbitur(abit, city, arKey=[], count=0, a=0, p=0, s=0, pm=0, lm=0):
    conn = psycopg2.connect(dbname='abit', password='admin', user='postgres')
    cur = conn.cursor()
    toBd = [0, 0, 0, 0, 0, 0, 0, '', '', '', '', 0, 0, ''];
    for (key, abitur) in abit.items():
        if key == 'personal':
            for (kee, abu) in abitur.items():
                toBd[1] = abit['sex']
                toBd[7] = abit['first_name']
                toBd[8] = abit['last_name']
                toBd[9] = abit['nickname']
                if kee == 'city':
                    toBd[10] = abit['city']['id']
                    toBd[13] = abit['city']['title']
                else:
                    toBd[10] = city
                    cur.execute('SELECT title FROM cities WHERE id = %s', (city,))
                    title = cur.fetchall()
                    toBd[13] = title[0][0]
                toBd[11] = abit['id']
                toBd[12] = 0
                if kee == 'religion':
                    toBd[0] = abit['personal']['religion']
                else:
                    toBd[0] = ""
                if kee == 'alcohol':
                    toBd[2] = abit['personal']['alcohol']
                    count += 1
                    a = 1
                if kee == 'political':
                    toBd[3] = abit['personal']['political']
                    count += 1
                    p = 1
                if kee == 'smoking':
                    toBd[4] = abit['personal']['smoking']
                    count += 1
                    s = 1
                if kee == 'people_main':
                    toBd[5] = abit['personal']['people_main']
                    count += 1
                    pm = 1
                if kee == 'life_main':
                    toBd[6] = abit['personal']['life_main']
                    count += 1
                    lm = 1
        if toBd[0] == "" or toBd[0] == 0:
            toBd[0] = 0
        elif toBd[0] == "Иудаизм":
            toBd[0] = 1
        elif toBd[0] == "Православие":
            toBd[0] = 2
        elif toBd[0] == "Католицизм":
            toBd[0] = 3
        elif toBd[0] == "Протестантизм":
            toBd[0] = 4
        elif toBd[0] == "Ислам":
            toBd[0] = 5
        elif toBd[0] == "Буддизм":
            toBd[0] = 6
        elif toBd[0] == "Конфуцианство":
            toBd[0] = 7
        elif toBd[0] == "Светский гуманизм":
            toBd[0] = 8
        elif toBd[0] == "Пастафарианство":
            toBd[0] = 9
        else:
            toBd[0] = 10
        if count >= 4:
            if a == 0:
                toBd[2] = 0
            if p == 0:
                toBd[3] = 0
            if s == 0:
                toBd[4] = 0
            if pm == 0:
                toBd[5] = 0
            if lm == 0:
                toBd[6] = 0
            toTrain = [
                [toBd[3], toBd[2], toBd[0],
                 toBd[4], toBd[6],
                 toBd[5], toBd[1]]]
            toBd[12] = predictModel(toTrain)


            cur.execute("""INSERT INTO abiturient(id,"firstName", "lastName", "middleName", 
                                    political, sex, alcohol, smoking,people_main, life_main, religion, "idSide", "idCity", city)
                                    VALUES ('{id}','{firstName}','{lastName}','{middleName}','{political}','{sex}',
                                    '{alcohol}','{smoking}','{people_main}','{life_main}','{religion}','{idSide}',
                                    '{idCity}','{city}')""". \
                        format(id=toBd[11], firstName=toBd[7], lastName=toBd[8],
                               middleName=toBd[9], political=toBd[3],
                               sex=toBd[1], alcohol=toBd[2], smoking=toBd[4],
                               people_main=toBd[5], life_main=toBd[6],
                               religion=toBd[0], idSide=int(toBd[12]),
                               idCity=toBd[10], city=toBd[13]))
            conn.commit()
            count = 0
            a = 0
            p = 0
            s = 0
            pm = 0
            lm = 0


def getAbitur():
    abiturs = None
    try:
        abiturs = db.session. \
            query(abiturient.id)
    except SQLAlchemyError as e:
        flash('There was error while querying database', 'danger')
        abort(500)
    return abiturs.all()

# составляем массив городов
def arCity(side):
    city = None
    try:
        city = db.session. \
            query(abiturient.city, abiturient.idCity). \
            distinct(abiturient.city). \
            filter(abiturient.idSide == side)
    except SQLAlchemyError as e:
        flash('There was error while querying database', 'danger')
        abort(500)
    return city


# составляем массив абитуриентов
def arEnrollee(side):
    abitur = None
    try:
        abitur = db.session. \
            query(abiturient). \
            filter(abiturient.idSide == side)
    except SQLAlchemyError as e:
        flash('There was error while querying database', 'danger')
        abort(500)
    return abitur


@module.route('/humanities', methods=['GET'])
def view_hum():
    enrollee = arEnrollee(1)
    city = arCity(1)
    return render_template('entrants/humanities.html', enrolles=enrollee, cities=city)


@module.route('/technical', methods=['GET'])
def view_tec():
    enrollee = arEnrollee(2)
    city = arCity(2)
    return render_template('entrants/technical.html', enrolles=enrollee, cities=city)


@module.route('/natural', methods=['GET'])
def view_nat():
    enrollee = arEnrollee(3)
    city = arCity(3)

    return render_template('entrants/natural.html', enrolles=enrollee, cities=city)
