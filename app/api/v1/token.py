from flask import current_app

from app.forms.client import ClientForm, EmailTokenForm
from app.lib.enums import ClientTypeEnum
from app.lib.errors import Success
from app.lib.module import Module
from app.lib.token import generate_token, TokenObj
from app.models.user import User

token_module = Module('token')


def __get_email_token():

    form = EmailTokenForm().validate_for_api()
    client_method = {
        ClientTypeEnum.USER_EMAIL: User.verify_email,
        ClientTypeEnum.USER_MOBILE: User.verify_mobile,
        ClientTypeEnum.USER_MINA: User.verify_mina,
        ClientTypeEnum.USER_WX: User.verify_wx
    }
    client_type = form.client_type.data
    user_id = client_method[client_type](form.account.data, form.password.data)
    token = generate_token(TokenObj(
        user_id, client_type.value), expiration=current_app.config['TOKEN_EXPIRATION']).decode(encoding='ascii')

    return Success().append(token=token)


def __get_mobile_token():
    pass


def __get_wx_token():
    pass


def __get_mina_token():
    pass


@token_module.route('', methods=['GET'])
def get():
    form = ClientForm().validate_for_api()
    client_method = {
        ClientTypeEnum.USER_EMAIL: __get_email_token,
        ClientTypeEnum.USER_MOBILE: __get_mobile_token,
        ClientTypeEnum.USER_WX: __get_wx_token,
        ClientTypeEnum.USER_MINA: __get_mina_token
    }
    client_type = form.client_type.data
    return client_method[client_type]()
