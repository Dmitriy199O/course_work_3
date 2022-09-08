import base64
import hashlib
import hmac

from werkzeug.exceptions import MethodNotAllowed

from app.dao.models.user import User
from app.dao.services.base import BaseService
from app.dao.services.exceptions import UserNotFound, WrongPassword

from flask import current_app


class UserService(BaseService):

    def get_by_email(self, email: str) -> User:
        user = self.dao.get_by_email(email)
        return user

    def create(self, data) -> User:
        user = self.dao.get_by_email(data.get('email'))
        data['password'] = self.get_hash(data.get('password'))
        user = self.dao.create(data)
        return user

    def get_hash(self, password: str) -> str:
        hash_p = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            current_app.config.get('PWD_HASH_SALT'),
            current_app.config.get('PWD_HASH_ITERATIONS')

        )
        return base64.b64encode(hash_p).decode('utf-8')

    # def hash_password(self, password: str) -> bytes:
    #     hash_digest = self.create_hash(password)
    #     encoded_digest = base64.b64encode(hash_digest)
    #     return encoded_digest

    # def create_hash(self, password: str) -> bytes:
    #
    #     hash_digest: bytes = hashlib.pbkdf2_hmac(
    #         'sha256',
    #         password.encode('utf-8'),
    #         current_app.config.get('PWD_HASH_SALT'),
    #         current_app.config.get('PWD_HASH_ITERATIONS')
    #     )
    #     return hash_digest

    def compare_passwords(self, password_hash: str, password_passed: str) -> bool:

        passed_hash = self.get_hash(password_passed)

        return hmac.compare_digest(password_hash, passed_hash)

    def update_user_info(self, data: dict, email: str) -> None:
        if not self.get_by_email(email):
            raise UserNotFound
        if 'password' not in data.keys() and 'email' not in data.keys():
            self.dao.update_by_email(data, email)
        else:
            raise MethodNotAllowed

    # def update_password(self, data: dict, email: str) -> None:
    #
    #     user = self.get_by_email(email)
    #     current_password = data.get('old_password')
    #     new_password = data.get('new_password')
    #
    #     if None in [current_password, new_password]:
    #         raise MethodNotAllowed
    #
    #     if not self.compare_passwords(user.password, current_password):
    #         raise WrongPassword
    #
    #     data = {
    #         'password': self.get_hash(new_password)
    #     }
    #     self.dao.update_by_email(data, email)

    def update_password(self, email, old_password, new_password):
        user = self.get_by_email(email)
        pwd_hash = self.get_hash(old_password)
        if pwd_hash != user.password:
            raise Exception('Invalid password')
        user.password = self.get_hash(new_password)
        return self.dao.update(user)
