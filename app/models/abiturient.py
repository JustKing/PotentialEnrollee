from slugify import slugify
from sqlalchemy import event

from app.database import db

class abiturient(db.Model):
    __tablename__ = 'abiturient'

    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    middleName = db.Column(db.String(100), nullable=False)


    def __str__(self):
        return self.id