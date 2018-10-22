from slugify import slugify
from sqlalchemy import event
from sqlalchemy.schema import ForeignKey

from app.database import db

class Abitur_inf(db.Model):
    #__tablename__ = 'enroleeinformation'
    __tablename__ = 'abitur_inf'

    abitur_id = db.Column(db.Integer, ForeignKey('abitur.id'), primary_key=True)
    political = db.Column(db.String(100))
    alcohol = db.Column(db.String(100))
    religion = db.Column(db.String(100))
    smoking = db.Column(db.String(100))
    life_main = db.Column(db.String(100))
    people_main = db.Column(db.String(100))
    sex = db.Column(db.Integer)

    def __str__(self):
        return self.name


@event.listens_for(Abitur_inf, 'before_insert')
def event_before_insert(mapper, connection, target):
    target.slug = slugify(target.name)


@event.listens_for(Abitur_inf, 'before_update')
def event_before_update(mapper, connection, target):
    target.slug = slugify(target.name)
