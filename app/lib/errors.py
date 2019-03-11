from app.lib.exception import APIException


class Success(APIException):
    code = 201
    msg = '成功'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 1
    msg = '删除成功'


class ServerError(APIException):
    code = 500
    msg = '服务器返回了一个未知错误'
    error_code = 999


class ParameterException(APIException):
    code = 400
    msg = '参数错误'
    error_code = 1000


class NotFound(APIException):
    code = 404
    msg = '资源未找到'
    error_code = 1001


class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = '验证失败'


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = '权限不够，禁止访问'

# 定义自己的异常
# class DuplicateGift(APIException):
#     code = 400
#     error_code = 2001
#     msg = '当前书籍已存在于礼物清单中'
