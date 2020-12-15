import datetime

from flask_restful import Resource, reqparse
from flask import request, jsonify, make_response
from server.constant import Constant
from ..model.schema.user_schema import UserSchema
from ..model.model.user_model import User
import jwt
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from server import db

from flask import current_app as app

from server.utils.bcript_password import Bcript_password


class Login_controler(Resource):

    def post(self):
        data = request.get_json()
        if not data or not data["email"] or not data["password"]:
            return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value

        user = User.query.filter_by(email=data["email"]).first()
        if not user or not Bcript_password.compare( data["password"], user.password):
            return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value

        token = jwt.encode(
            {
                'id': user.id,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            },
            app.config["SECRET_KEY"],
        )
        user_schema = UserSchema(many=False)
        return_user = user_schema.dump(user)
        return make_response({
            'token': token.decode('utf-8'),
            'payload': return_user
        }, Constant.STATUS_CODE.OK.value)