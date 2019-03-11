from app.forms.client import ClientForm, EmailForm
from app.lib.errors import Success
from app.lib.module import Module
from app.lib.enums import ClientTypeEnum
from app.models.user import User

client_module = Module('client')


def __register_user_email():
    email_form = EmailForm()
    email_form.validate_for_api()
    user_id = User.create(email_form.nickname.data,
                          email_form.account.data,
                          email_form.password.data)
    return Success().append(user_id=user_id)


def __register_user_mobile():
    pass


def __register_user_mina():
    pass


def __register_user_wx():
    pass


@client_module.route('',  methods=['POST'])
def create():
    client_form = ClientForm().validate_for_api()
    client_method = {
        ClientTypeEnum.USER_EMAIL: __register_user_email,
        ClientTypeEnum.USER_MOBILE: __register_user_mobile,
        ClientTypeEnum.USER_MINA: __register_user_mina,
        ClientTypeEnum.USER_WX: __register_user_wx
    }
    client_type = client_form.client_type.data
    return client_method[client_type]()
