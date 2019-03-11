from flask import g

from app.lib.errors import Success
from app.lib.module import Module
from app.lib.token import auth
from app.lib.scopes import check_scope
from app.models.user import User
from app.models import db

user_module = Module('user')


@user_module.route('', methods=['GET'])
@auth.login_required
@check_scope
def get_user():
    user = g.user
    return Success().append(user=user)


@user_module.route('/<int:user_id>', methods=['GET'])
@auth.login_required
@check_scope
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    return Success().append(user=user)


@user_module.route('', methods=['DELETE'])
@auth.login_required
@check_scope
def delete():
    user_id = g.user.id
    with db.auto_commit():
        user = User.query.get_or_404(user_id)
        user.delete()
    return Success()


@user_module.route('/<int:id>', methods=['DELETE'])
@auth.login_required
@check_scope
def delete_user(user_id):
    with db.auto_commit():
        user = User.query.get_or_404(user_id)
        user.delete()
    return Success()
