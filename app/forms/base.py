from wtforms import Form as _Form
from app.lib.errors import ParameterException
from flask import request


class Form(_Form):
    def __init__(self):
        data = request.json
        args = request.args.to_dict()
        super().__init__(data=data, **args)

    def validate_for_api(self):
        if not self.validate():
            raise ParameterException(msg=self.errors)

        return self
