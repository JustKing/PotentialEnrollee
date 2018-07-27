from slugify import slugify
from sqlalchemy import event
from sqlalchemy.schema import ForeignKey

from app.database import db

class Abitur_inf(db.Model):
    __tablename__ = 'abitur_inf'

    id = db.Column(db.Integer, primary_key=True)
    political = db.Column(db.String(100))
    alcohol = db.Column(db.String(100))
    religion = db.Column(db.String(100))
    smoking = db.Column(db.String(100))
    life_main = db.Column(db.String(100))
    people_main = db.Column(db.String(100))
    sex = db.Column(db.Integer)
    comment = db.Column(db.String(1000))
    id_abitur = db.Column(db.Integer, ForeignKey('abitur.id'))
    id_status = db.Column(db.Integer, ForeignKey('status.id'))

    #abitur_inf = db.relationship('abitur_inf', backref='abitur')

    def __str__(self):
        return self.name


@event.listens_for(Abitur_inf, 'before_insert')
def event_before_insert(mapper, connection, target):
    # Здесь будет очень важная бизнес логика
    # Или нет. На самом деле, старайтесь использовать сигналы только
    # тогда, когда других, более правильных вариантов не осталось.
    target.slug = slugify(target.name)


@event.listens_for(Abitur_inf, 'before_update')
def event_before_update(mapper, connection, target):
    target.slug = slugify(target.name)
