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


def saveAbitur(abit, arKey=[], count=0):
    print(abit)
    for (key, abitur) in abit.items():
        if key == 'personal':
            for (k, ab) in abitur.items():
                if k == 'religion':
                    if ab == "" or ab == 0:
                        abit['personal']['religion'] = 0
                    elif ab == "Иудаизм":
                        abit['personal']['religion'] = 1
                    elif ab == "Православие":
                        abit['personal']['religion'] = 2
                    elif ab == "Католицизм":
                        abit['personal']['religion'] = 3
                    elif ab == "Протестантизм":
                        abit['personal']['religion'] = 4
                    elif ab == "Ислам":
                        abit['personal']['religion'] = 5
                    elif ab == "Буддизм":
                        abit['personal']['religion'] = 6
                    elif ab == "Конфуцианство":
                        abit['personal']['religion'] = 7
                    elif ab == "Светский гуманизм":
                        abit['personal']['religion'] = 8
                    elif ab == "Пастафарианство":
                        abit['personal']['religion'] = 9
                    else:
                        abit['personal']['religion'] = 10
                    for (ke, abitu) in abit.items():
                        if key == 'personal':
                            for (kee, abu) in abitu.items():
                                if kee == 'alcohol':
                                    count += 1
                                if kee == 'political':
                                    count += 1
                                if kee == 'smoking':
                                    count += 1
                                if kee == 'people_main':
                                    count += 1
                                if kee == 'life_main':
                                    count += 1
                    print(count, 'COUNT PIZDETC NAXUY BLYAT')
                # if count > 1:
                #     if k != 'alcohol':
                #         if k not in arKey:
                #             abit['personal']['alcohol'] = 0
                #     if k != 'political':
                #         if k not in arKey:
                #             abit['personal']['political'] = 0
                #     if k != 'smoking':
                #         if k not in arKey:
                #             abit['personal']['smoking'] = 0
                #     if k != 'people_main':
                #         if k not in arKey:
                #             abit['personal']['people_main'] = 0
                #     if k != 'life_main':
                #         if k not in arKey:
                #             abit['personal']['life_main'] = 0
                #     if k != 'religion':
                #         if k not in arKey:
                #             abit['personal']['religion'] = 0
                #     arKey.append(k)
                #
                #     print(arKey)
                    print(abit)
                    toTrain = [[abit['personal']['political'], abit['personal']['alcohol'], abit['personal']['religion'],
                                abit['personal']['smoking'], abit['personal']['life_main'],
                                abit['personal']['people_main'], abit['sex']]]
                    side = predictModel(toTrain)

                    abitur = abiturient(id=abit['id'],
                                        firstName=abit['first_name'],
                                        lastName=abit['last_name'],
                                        middleName=abit['nickname'],
                                        political=abit['personal']['political'],
                                        sex=abit['sex'],
                                        alcohol=abit['personal']['alcohol'],
                                        smoking=abit['personal']['smoking'],
                                        people_main=abit['personal']['people_main'],
                                        life_main=abit['personal']['life_main'],
                                        religion=abit['personal']['religion'],
                                        idSide=int(side)
                                        )
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
            query(abiturient.id)
    except SQLAlchemyError as e:
        flash('There was error while querying database', 'danger')
        abort(500)
    return abiturs.all()
