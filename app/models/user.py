from sqlalchemy import Column, String, Integer, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash

from app.lib.errors import AuthFailed
from app.models import db, Base
from app.lib.mixin import ConvertToDictMixin


class User(Base, db.Model, ConvertToDictMixin):
    id = Column(Integer, primary_key=True)
    email = Column(String(36), unique=True, nullable=False)
    nickname = Column(String(36), unique=True)
    auth = Column(SmallInteger, default=1)
    _password = Column('password', String(128))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'email', 'nickname']

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)

    @classmethod
    def create(cls, nickname, email, password):
        user = cls()
        with db.auto_commit():
            user.nickname = nickname
            user.email = email
            user.password = password
            db.session.add(user)
        return user.id

    @staticmethod
    def has_register(email):
        if User.query.filter_by(email=email).first():
            return True
        else:
            return False

    @classmethod
    def verify_email(cls, email, password):
        user = cls.query.filter_by(email=email).first_or_404()
        if not user.check_password(password):
            raise AuthFailed('用户名或密码不正确')
        return user.id

    @staticmethod
    def verify_mobile():
        pass

    @staticmethod
    def verify_mina():
        pass

    @staticmethod
    def verify_wx():
        pass
