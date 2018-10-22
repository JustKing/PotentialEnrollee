from slugify import slugify
from sqlalchemy import event, ForeignKey

from app.database import db

class abiturient(db.Model):
    __tablename__ = 'abiturient'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    middleName = db.Column(db.String(100), nullable=False)
    political =db.Column(db.String(100))
    sex =db.Column(db.Integer)
    alcohol =db.Column(db.String(100))
    smoking =db.Column(db.String(100))
    people_main =db.Column(db.String(100))
    life_main =db.Column(db.String(100))
    religion =db.Column(db.String(100))
    idSide =db.Column(db.Integer, ForeignKey('side.id'))


    def __str__(self):
        return self.id