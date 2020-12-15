from flask_restful import Resource, reqparse
from flask import request, jsonify
from server.constant import Constant
from ..model.schema.user_schema import UserSchema
from ..model.model.user_model import User
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from server import db
from server.utils.bcript_password import Bcript_password
from ..security.authorization import token_required


class List_user_controler(Resource):
    @token_required
    def get(self, current_user):
        if current_user.role == Constant.ROLE["USER_ROLE"].user:
            return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value

        role_can_query = [Constant.ROLE["USER_ROLE"].user]

        if current_user.role == Constant.ROLE["USER_ROLE"].admin_root:
            role_can_query = [Constant.ROLE["USER_ROLE"].admin, Constant.ROLE["USER_ROLE"].user]

        try:
            result = []
            for role in role_can_query:
                get_users = User.query.filter_by(role=role)

                user_schema = UserSchema(many=True)
                users = user_schema.dump(get_users)
                for user in users:
                    user.pop("password", None)
                result += users
            return {"payload": result}, Constant.STATUS_CODE.OK.value
        except Exception as e:
            print(e)
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value

    def post(self):
        try:
            data = request.get_json()
            user_schema = UserSchema()
            user = user_schema.load(data)
            result = user_schema.dump(user.create())
            result.pop("password", None)
        except IntegrityError:
            return {"error": "User already exists"}, 409
        except ValidationError as e:
            return {"error": e.messages}, Constant.STATUS_CODE.BAD_REQUEST.value
        except Exception as e:
            print(e)
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value


        return {"payload": result} , Constant.STATUS_CODE.OK.value
