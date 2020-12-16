from flask_restful import Resource, reqparse
from flask import request, jsonify
from server.constant import Constant
from ..model.schema.book_schema import BookSchema

from ..model.model.book_model import Book
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from server import db

from ..security.authorization import token_required


class Book_controller(Resource):
    @token_required
    def get(self, current_user, book_id):
        if not current_user.role == Constant.ROLE["USER_ROLE"].admin_root and not current_user.role == Constant.ROLE["USER_ROLE"].MANAGER and not current_user.role == Constant.ROLE["USER_ROLE"].NHAN_VIEN:
                return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value
        try:
            get_book = Book.query.get(book_id)
            if get_book:
                book_schema = BookSchema(many=False)
                book = book_schema.dump(get_book)
                return {"payload": book}, Constant.STATUS_CODE.OK.value
            else:
                return {'error': Constant.STATUS_CODE.NOT_FOUND.name}, Constant.STATUS_CODE.NOT_FOUND.value
        except Exception as e:
            print(e)
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value

    @token_required
    def put(self, current_user, book_id):

        if not current_user.employee_functions == Constant.FUNCTIONS['EMPLOYEE'].THU_KHO:
            if not current_user.role == Constant.ROLE["USER_ROLE"].admin_root:
                return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value
        try:
            data = request.get_json()
            book = Book.query.get(book_id)
            if not book:
                return {'error': Constant.STATUS_CODE.NOT_FOUND.name}, Constant.STATUS_CODE.NOT_FOUND.value

            if data.get('name'):
                book.name = data['name']
            if data.get('author'):
                book.author = data['author']
            if data.get('category'):
                book.category = data['category']
            if data.get('image'):
                book.category = data['image']

            db.session.add(book)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value

        book_schema = BookSchema(only=['name', 'author', 'category','image'])
        modify = book_schema.dump(book)
        return {"payload": modify},  Constant.STATUS_CODE.OK.value

    @token_required
    def delete(self, current_user, book_id):
        if not current_user.employee_functions == Constant.FUNCTIONS['EMPLOYEE'].THU_KHO:
            if not current_user.role == Constant.ROLE["USER_ROLE"].admin_root:
                return {"error": Constant.STATUS_CODE.UNAUTHORIZED.name}, Constant.STATUS_CODE.UNAUTHORIZED.value
        try:
            get_book = Book.query.get(book_id)
            if not get_book:
                return {'error': Constant.STATUS_CODE.NOT_FOUND.name}, Constant.STATUS_CODE.NOT_FOUND.value

            db.session.delete(get_book)
            db.session.commit()
            return "", Constant.STATUS_CODE.NO_CONTENT.value
        except Exception as e:
            db.session.rollback()
            print(e)
            return {"error": Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.name}, Constant.STATUS_CODE.INTERNAL_SERVER_ERROR.value
