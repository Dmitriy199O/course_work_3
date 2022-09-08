from flask import request, jsonify
from flask_restx import Namespace, Resource, abort
from app.container import movie_service
from app.dao.models.movie import MovieSchema
from app.dao.services.exceptions import ItemNotFound

movies_ns = Namespace('movies')

movies_schema = MovieSchema(many=True)
movie_schema = MovieSchema()


@movies_ns.route('/')
class MovieView(Resource):

    def get(self):
        page = request.args.get('pages')
        status = request.args.get('status')
        try:
            all_movies = movie_service.get_all(page, status)
            return movies_schema.dump(all_movies)
        except ItemNotFound:
            abort(404)


@movies_ns.route('/<int:mid>/')
class MovieView(Resource):

    def get(self, mid):
        try:
            movie = movie_service.get_one(mid)

            return movie_schema.dump(movie), 200
        except ItemNotFound:
            abort(404)