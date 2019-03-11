from enum import Enum


class ClientTypeEnum(Enum):
    USER_EMAIL = 100
    USER_MOBILE = 101

    # 微信小程序
    USER_MINA = 200
    # 微信公众号
    USER_WX = 201

    @classmethod
    def check_type(cls, client_type):
        try:
            client_enum = cls(client_type)
        except ValueError as e:
            raise e
        return client_enum


class ScopeTypeEnum(Enum):
    NORMAL_USER = 1
    ADMIN = 2

    @classmethod
    def reflect_scope(cls, scope_type):
        try:
            scope_type_enum = cls(scope_type)
        except ValueError as e:
            raise e

        from app.lib.scope import Scope
        from app.lib.scopes import UserScope, AdminScope

        scope_dict = {
            cls.NORMAL_USER: UserScope,
            cls.ADMIN: AdminScope
        }

        return scope_dict.get(scope_type_enum, Scope)()
