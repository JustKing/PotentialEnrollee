from slugify import slugify
from sqlalchemy import event
from sqlalchemy.schema import ForeignKey

from app.database import db

class Place(db.Model):
    __tablename__ = 'place'

    id = db.Column(db.Integer, primary_key=True)
    id_city = db.Column(db.Integer, ForeignKey('city.id'))

    def __str__(self):
        return self.name


@event.listens_for(Place, 'before_insert')
def event_before_insert(mapper, connection, target):
    target.slug = slugify(target.name)


@event.listens_for(Place, 'before_update')
def event_before_update(mapper, connection, target):
    target.slug = slugify(target.name)
