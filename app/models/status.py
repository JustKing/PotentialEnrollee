from slugify import slugify
from sqlalchemy import event

from app.database import db

class Status(db.Model):
    __tablename__ = 'status'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))

    def __str__(self):
        return self.name
