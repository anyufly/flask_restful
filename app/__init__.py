from flask import Flask as _Flask
from flask.json import JSONEncoder as _JSONEncoder


class JSONEncoder(_JSONEncoder):

    def default(self, o):
        try:
            rv = super(JSONEncoder, self).default(o)
            return rv
        except TypeError:
            try:
                return dict(o)
            except TypeError as e:
                raise e


class Flask(_Flask):
    json_encoder = JSONEncoder


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.setting')
    app.config.from_object('app.secure')
    register_blueprint(app)
    return app


def register_blueprint(app):
    from app.api.v1 import bp_v1
    from app.api.v1.user import user_module
    from app.api.v1.client import client_module
    from app.api.v1.token import token_module
    # 要将注册模块的代码写在注册蓝图前面
    user_module.register_to_bp(bp_v1)
    client_module.register_to_bp(bp_v1)
    token_module.register_to_bp(bp_v1)
    app.register_blueprint(bp_v1)


def register_db(app, db):
    db.init_app(app)
    with app.app_context():
        db.create_all()
