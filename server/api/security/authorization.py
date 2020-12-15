from functools import wraps
from server.constant import Constant
from flask import request
import jwt
from flask import current_app as app
from ..model.model.user_model import User

def token_required(f):
    @wraps(f)
    def decorated(self, *args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"])
            current_user = User.query.filter_by(id=data["id"]).first()
        except Exception as e:
            print(e)
            return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value
        return f(self,current_user, *args, **kwargs)

    return decorated