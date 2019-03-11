from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired, BadSignature
from flask import current_app, g
from app.lib.errors import AuthFailed
from flask_httpauth import HTTPBasicAuth
from app.models.user import User

auth = HTTPBasicAuth()


class TokenObj:
    def __init__(self, user_id, client_type, scope=None):
        self.user_id = user_id
        self.client_type = client_type
        if scope:
            self.scope = scope
        self.key_items = ['user_id', 'client_type', 'scope']

    def keys(self):
        return self.key_items

    def __getitem__(self, item):
        return getattr(self, item, '')


@auth.verify_password
def verify_password(account, password):
    # HttpBaseAuth标准（在header中写入）
    # key=Authorization
    # value =basic base64(qiyue:123456) 需要对账号密码进行base64加密
    token_obj = check_token(account)
    user = User.query.get_or_404(token_obj.user_id)

    g.user = user
    return True


def generate_token(token: TokenObj, expiration=7200):
    serializer = TimedJSONWebSignatureSerializer(
        secret_key=current_app.config['SECRET_KEY'], expires_in=expiration)
    return serializer.dumps(dict(token))


def check_token(token):
    serializer = TimedJSONWebSignatureSerializer(secret_key=current_app.config['SECRET_KEY'])
    try:
        token_obj = serializer.loads(token)
    except SignatureExpired:
        raise AuthFailed(msg='token已过期', error_code=1003)
    except BadSignature:
        raise AuthFailed(msg='token无效', error_code=1002)

    return TokenObj(token_obj['user_id'], token_obj['client_type'], token_obj['scope'])
