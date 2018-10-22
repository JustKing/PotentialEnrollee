from slugify import slugify
from sqlalchemy import event

from app.database import db

class Enrollee(db.Model):
    __tablename__ = 'enrollee'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    middleName = db.Column(db.String(100), nullable=False)
    idSide = db.Column(db.Integer)
    city = db.Column(db.Integer)
    idCity = db.Column(db.String(100))
    bdate = db.Column(db.String(11))

    def __str__(self):
        return self.name


@event.listens_for(Enrollee, 'before_insert')
def event_before_insert(mapper, connection, target):
    target.slug = slugify(target.name)


@event.listens_for(Enrollee, 'before_update')
def event_before_update(mapper, connection, target):
    target.slug = slugify(target.name)
