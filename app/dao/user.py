from typing import Union
from sqlalchemy.exc import NoResultFound
from app.dao.base import BaseDAO
from app.dao.models.user import User


class UserDAO(BaseDAO):

    def get_by_email(self, email: str) -> Union[User, None]:
        try:
            user = self.session.query(User).filter(User.email == email).one()
            return user
        except NoResultFound:
            return None

    def create(self, data):
        new_user = User(**data)

        self.session.add(new_user)
        self.session.commit()

        return new_user

    def update_by_email(self, data: dict, email: str) -> None:
        self.session.query(User).filter(User.email == email).update(data)
        self.session.commit()

    def update(self, user):
        self.session.add(user)
        self.session.commit()
