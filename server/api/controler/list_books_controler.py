from flask_restful import Resource, reqparse
from flask import request, jsonify
from server.constant import Constant
from ..model.schema.book_schema import BookSchema
from ..model.model.book_model import Book
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from server import db
from server.utils.bcript_password import Bcript_password
from ..security.authorization import token_required


class List_books_controller(Resource):
    @token_required
    def get(self, current_user):
        if not current_user.role == Constant.ROLE["USER_ROLE"].admin_root and not current_user.role == Constant.ROLE["USER_ROLE"].MANAGER and not current_user.role == Constant.ROLE["USER_ROLE"].NHAN_VIEN:
            return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value

        try:

            get_books = Book.query.all()

            book_schema = BookSchema(many=True)
            book = book_schema.dump(get_books)
            return {"payload": book}, Constant.STATUS_CODE.OK.value
        except Exception as e:
            print(e)
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value

    @token_required
    def post(self, current_user):
        if not current_user.employee_functions == Constant.FUNCTIONS['EMPLOYEE'].THU_KHO:
            if not current_user.role == Constant.ROLE["USER_ROLE"].admin_root:
                return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value
        try:
            data = request.get_json()
            data['user_id'] = current_user.id
            book_schema = BookSchema()
            book = book_schema.load(data)
            result = book_schema.dump(book.create())
        except IntegrityError:
            return {"error": "Book already exists"}, 409
        except ValidationError as e:
            return {"error": e.messages}, Constant.STATUS_CODE.BAD_REQUEST.value
        except Exception as e:
            print(e)
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value


        return {"payload": result} , Constant.STATUS_CODE.OK.value
