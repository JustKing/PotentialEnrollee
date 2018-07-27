from slugify import slugify
from sqlalchemy import event

from app.database import db

class newAbitur(db.Model):
    __tablename__ = 'newabitur'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    middle_name = db.Column(db.String(100), nullable=False)


    def __str__(self):
        return self.id