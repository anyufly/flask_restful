from werkzeug.exceptions import HTTPException
from flask import request
from app.lib.mixin import ConvertToDictMixin


class APIException(HTTPException, ConvertToDictMixin):

    code = 500
    msg = '对不起，发生了内部错误'
    error_code = 999

    def __init__(self, code=None, error_code=None, msg=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg

        self.fields = ['error_code', 'msg', 'request']
        self.request = request.method + ' ' + self.get_url_no_param()
        super(APIException, self).__init__(msg, None)

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    def get_body(self, environ=None):
        from flask.json import dumps
        return dumps(dict(self))

    @staticmethod
    def get_url_no_param():
        full_path = request.full_path
        main_path = full_path.split('?')
        return main_path[0]
