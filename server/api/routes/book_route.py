from flask import current_app as app
from flask_restful import Api

from server.config import Config
from ..controler.book_controler import Book_controller
from ..controler.list_books_controler import List_books_controller
from ..controler.login_controller import Login_controler


api = Api(app)

# Router for User
api.add_resource(Book_controller, Config.ROUTE['API']["BOOK"])
api.add_resource(List_books_controller, Config.ROUTE['API']["BOOKS"])


