from marshmallow_sqlalchemy import ModelSchema
from ..model.user_model import User
from marshmallow import fields, pre_load, ValidationError
from server import db
from server.constant import Constant

from server.utils.bcript_password import Bcript_password


class UserSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = User
        sqla_session = db.session
    id = fields.Integer(dump_only=True)
    email = fields.Email(required=True)
    password = fields.String(required=True)
    firstname = fields.String(required=True)
    lastname = fields.String(required=True)
    avatar = fields.String(default="", missing= "")
    role = fields.String(default=Constant.ROLE["USER_ROLE"].user.value, missing=Constant.ROLE["USER_ROLE"].user.value)
    created_at = fields.DateTime()
    updated_at = fields.DateTime()

    @pre_load
    def preprocess(self, data, **kwargs):
        if "password" in data:
            data["password"] = Bcript_password.hash(data["password"])
        return data
