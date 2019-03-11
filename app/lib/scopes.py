from app.lib.scope import Scope
from app.lib.enums import ScopeTypeEnum
from app.lib.errors import Forbidden
from flask import g, request
from functools import wraps


def check_scope(func):
    @wraps(func)
    def check(*args, **kwargs):
        user = g.user
        scope = ScopeTypeEnum.reflect_scope(user.auth)
        endpoint = request.endpoint
        if endpoint not in scope.result:
            raise Forbidden()
        return func(*args, **kwargs)
    return check


class UserScope(Scope):
    type = 1
    allow_func = ['v1.get', 'v1.get_user', 'v1.delete_user']
    allow_module = []
    forbidden_func = []
    forbidden_module = []


class AdminScope(Scope):
    type = 2
    allow_module = ['v1.user', 'v1.client', 'v1.token']
