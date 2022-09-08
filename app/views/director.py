from flask import request, jsonify
from flask_restx import Namespace, Resource, abort
from app.container import director_service
from app.dao.models.director import DirectorSchema
from app.dao.services.exceptions import ItemNotFound

director_ns = Namespace('directors')

directors_schema = DirectorSchema(many=True)
director_schema = DirectorSchema()


@director_ns.route('/')
class DirectorView(Resource):

    def get(self):
        page = request.args.get('page')
        try:
            all_directors = director_service.get_all()

            return directors_schema.dump(all_directors), 200
        except ItemNotFound:
            abort(404)


@director_ns.route('/<int:did>/')
class DirectorView(Resource):

    def get(self, did):
        try:
            director = director_service.get_one(did)

            return director_schema.dump(director), 200
        except ItemNotFound:
            abort(404)
