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


class User_controler(Resource):
    @token_required
    def get(self, current_user, user_id):
        if current_user.id != user_id:
            if not current_user.role == Constant.ROLE["USER_ROLE"].admin_root and not current_user.role == Constant.ROLE["USER_ROLE"].admin:
                return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value
        try:
            get_user = User.query.get(user_id)
            if get_user:
                user_schema = UserSchema(many=False)
                user = user_schema.dump(get_user)
                user.pop("password", None)
                return {"payload": user}, Constant.STATUS_CODE.OK.value
            else:
                return {'error': Constant.STATUS_CODE.NOT_FOUND.name}, Constant.STATUS_CODE.NOT_FOUND.value
        except Exception as e:
            print(e)
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value

    @token_required
    def put(self,current_user, user_id):
        if current_user.id != user_id:
            if not current_user.role == Constant.ROLE["USER_ROLE"].admin_root and not current_user.role == Constant.ROLE["USER_ROLE"].admin:
                return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value
        try:
            data = request.get_json()
            user = User.query.get(user_id)
            if not user:
                return {'error': Constant.STATUS_CODE.NOT_FOUND.name}, Constant.STATUS_CODE.NOT_FOUND.value

            if data.get('password'):
               user.password = Bcript_password.hash(data["password"])
            if data.get('firstname'):
                user.firstname = data['firstname']
            if data.get('lastname'):
                user.lastname = data['lastname']
            if data.get('avatar'):
                user.avatar = data['avatar']
            if data.get('role'):
                user.role = data["role"]
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value

        user_schema = UserSchema(only=['firstname', 'lastname', 'avatar','role'])
        usermodify = user_schema.dump(user)
        return {"payload": usermodify},  Constant.STATUS_CODE.OK.value

    @token_required
    def delete(self,current_user, user_id):
        if not current_user.role == Constant.ROLE["USER_ROLE"].admin_root and not current_user.role == Constant.ROLE["USER_ROLE"].admin:
            return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value
        try:
            get_user = User.query.get(user_id)
            if not get_user:
                return {'error': Constant.STATUS_CODE.NOT_FOUND.name}, Constant.STATUS_CODE.NOT_FOUND.value

            db.session.delete(get_user)
            db.session.commit()
            return "", Constant.STATUS_CODE.NO_CONTENT.value
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value
