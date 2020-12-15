from flask import current_app as app
from flask_restful import Api

from server.config import Config
from ..controler.user_controler import User_controler
from ..controler.list_users_controler import List_user_controler
from ..controler.login_controller import Login_controler


api = Api(app)

# Router for User
api.add_resource(User_controler, Config.ROUTE['API']["USER"])
api.add_resource(List_user_controler, Config.ROUTE['API']["USERS"])
api.add_resource(Login_controler, Config.ROUTE['API']["LOGIN"])


