from slugify import slugify
from sqlalchemy import event

from app.database import db

class Area(db.Model):
    __tablename__ = 'area'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))

    def __str__(self):
        return self.name


@event.listens_for(Area, 'before_insert')
def event_before_insert(mapper, connection, target):
    # Здесь будет очень важная бизнес логика
    # Или нет. На самом деле, старайтесь использовать сигналы только
    # тогда, когда других, более правильных вариантов не осталось.
    target.slug = slugify(target.name)


@event.listens_for(Area, 'before_update')
def event_before_update(mapper, connection, target):
    target.slug = slugify(target.name)
