from app import create_app, register_db
from app.models import db
from app.lib.exception import APIException
from app.lib.errors import ServerError
from werkzeug.exceptions import HTTPException
app = create_app()
register_db(app, db)


@app.errorhandler(Exception)
def common_error_handler(e):
    if isinstance(e, APIException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = '1007'
        return APIException(code, msg, error_code)
    else:
        if app.config['DEBUG']:
            raise e
        else:
            return ServerError()


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
