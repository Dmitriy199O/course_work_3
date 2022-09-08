from typing import Callable
import datetime
import jwt

from flask import current_app, request, abort
from app.dao.services.exceptions import InvalidToken, WrongPassword
from app.dao.services.user import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, credentials, is_refresh=False) -> dict:

        email_passed = credentials.get('email')
        password_passed = credentials.get('password')
        user = self.user_service.get_by_email(email_passed)

        if not is_refresh:

            password_is_correct = self.user_service.compare_passwords(user.password, password_passed)
            if not password_is_correct:
                raise WrongPassword

        data = {
            'email': user.email,
        }

        access_token = jwt.encode(data, current_app.config['JWT_SECRET'],
                                  current_app.config['JWT_ALGORITHM'])

        data['exp'] = datetime.datetime.utcnow() + datetime.timedelta(days=current_app.config['TOKEN_EXPIRE_DAYS'])

        refresh_token = jwt.encode(data, current_app.config['JWT_SECRET'],
                                   current_app.config['JWT_ALGORITHM'])

        return {
            'access_token': access_token,
            'refresh_token': refresh_token
        }

    def get_email_from_jwt(self, token: str) -> dict:
        try:
            data = jwt.decode(token, current_app.config['JWT_SECRET'], current_app.config['JWT_ALGORITHM'])
            return data.get('email')
        except Exception:
            raise InvalidToken

    def approve_token(self, refresh_token: str) -> dict:

        credentials = {
            'email': self.get_email_from_jwt(refresh_token),
            'password': None
        }
        new_tokens = self.generate_tokens(credentials, is_refresh=True)
        return new_tokens

    @staticmethod
    def auth_required(func: Callable):
        def wrapper(*args, **kwargs):
            if 'Authorization' not in request.headers:
                abort(401)

            data = request.headers['Authorization']
            token = data.split('Bearer ')[-1]
            try:
                jwt.decode(token, current_app.config['JWT_SECRET'], current_app.config['JWT_ALGORITHM'])
            except Exception as e:
                print('JWT encode exception', e)
                abort(401)

            return func(*args, **kwargs)

        return wrapper
