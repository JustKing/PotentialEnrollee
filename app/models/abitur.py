from slugify import slugify
from sqlalchemy import event

from app.database import db

class Abitur(db.Model):
    __tablename__ = 'abitur'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100), nullable=False)
    id_side = db.Column(db.Integer)
    city = db.Column(db.Integer)
    city_id = db.Column(db.String(100))
    bdate = db.Column(db.String(11))

    #abitur_inf = db.relationship('abitur_inf', backref='abitur')

    def __str__(self):
        return self.name


@event.listens_for(Abitur, 'before_insert')
def event_before_insert(mapper, connection, target):
    # Здесь будет очень важная бизнес логика
    # Или нет. На самом деле, старайтесь использовать сигналы только
    # тогда, когда других, более правильных вариантов не осталось.
    target.slug = slugify(target.name)


@event.listens_for(Abitur, 'before_update')
def event_before_update(mapper, connection, target):
    target.slug = slugify(target.name)
