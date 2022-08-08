from marshmallow import Schema, fields
from app.create_db import db
from app.dao.models.base import BaseModel
from app.dao.models.genre import Genre


class User(BaseModel, db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(255))
    surname = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(255))
    favourite_genre = db.Column(db.ForeignKey(Genre.id))
    genre = db.relationship('Genre')


class UserSchema(Schema):
    id = fields.Int()
    username = fields.Str()
    surname = fields.Str()
    email = fields.Str()
    # password = fields.Str()
    role = fields.Str()
