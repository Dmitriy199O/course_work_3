from flask import request, abort
from flask_restx import Namespace, Resource
from werkzeug.exceptions import MethodNotAllowed

from app.container import user_service, auth_service
from app.dao.models.user import UserSchema
from app.dao.services.exceptions import UserNotFound, WrongPassword, ValidationError

user_ns = Namespace('user')

users_schema = UserSchema(many=True)
user_schema = UserSchema()


@user_ns.route('/')
class UserView(Resource):

    def get(self):
        try:
            auth_data = request.headers['Authorization']
            token = auth_data.split("Bearer ")[-1]
            email = auth_service.get_email_from_jwt(token)
            user = user_service.get_by_email(email)
            user_dict = user_schema.dump(user)
            return user_dict, 200

        except UserNotFound:
            abort(404, 'User not found')


@auth_service.auth_required
def patch(self):
    try:
        auth_data = request.headers['Authorization']
        token = auth_data.split("Bearer ")[-1]
        email = auth_service.get_email_from_jwt(token)
        updated_data = user_schema.dump(request.json)
        user_service.update_user_info(updated_data, email)
        return "", 200

    except MethodNotAllowed:
        abort(405, "You're not allowed to change the data passed")
    except UserNotFound:
        abort(404, 'User not found')
    except ValidationError:
        abort(400, 'Wrong fields passed')


@user_ns.route('/password/')
class PasswordView(Resource):

    # def put(self):
    #     try:
    #         auth_data = request.headers['Authorization']
    #         token = auth_data.split("Bearer ")[-1]
    #         email = auth_service.get_email_from_jwt(token)
    #         passwords = request.json
    #         user_service.update_password(passwords, email)
    #         return "", 200
    #     except UserNotFound:
    #         abort(404, 'User not found')
    #     except WrongPassword:
    #         abort(401, 'Incorrect password')
    @auth_service.auth_required
    def put(self):

        email = auth_service.get_email_from_jwt()
        user = user_service.get_by_email(email)

        old_password = request.json.get('old_password')
        new_password = request.json.get('new_password')

        user_service.update_password(user.email, old_password, new_password)

        return '', 204
