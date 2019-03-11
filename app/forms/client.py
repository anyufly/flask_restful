from wtforms import IntegerField, StringField
from app.forms.base import Form
from wtforms.validators import DataRequired, ValidationError, Length, Email, Regexp
from app.lib.enums import ClientTypeEnum
from app.models.user import User


class ClientForm(Form):
    client_type = IntegerField(validators=[DataRequired(message='未传入客户端类型')])
    account = StringField(validators=[DataRequired(message='未传入账户'), Length(
        min=2, max=32, message='账户的长度为2-32个字符'
    )])
    password = StringField(validators=[DataRequired(message='未传入密码')])

    def validate_client_type(self, field):
        client_type = field.data

        try:
            client_enum = ClientTypeEnum.check_type(client_type)
        except ValueError:
            raise ValidationError('传入的客户端类型错误')
        field.data = client_enum


class EmailTokenForm(ClientForm):
    account = StringField(validators=[
        Email(message='Email不合法')
    ])
    password = StringField(validators=[
        DataRequired('未传入密码'),
        Length(min=6, max=32),
        # password can only include letters , numbers and "_"
        Regexp(r'^[A-Za-z0-9_*&$#@]{6,32}$', message='密码只能由字母、数字和_组成')
    ])
    nickname = StringField(validators=[DataRequired(),
                                       Length(min=2, max=32, message='昵称的长度为2-32个字符')])


class EmailForm(EmailTokenForm):

    def validate_account(self, field):
        account = field.data
        if User.has_register(account):
            raise ValidationError('邮箱已被注册')
