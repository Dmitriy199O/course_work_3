from marshmallow import fields, Schema
from app.create_db import db
from app.dao.models.base import BaseModel


class Movie(BaseModel):
    __tablename__ = 'movie'
    title = db.Column(db.String(255), unique=True)
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Integer)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Str()
    genre_id = fields.Str()
    director_id = fields.Str()
