from marshmallow_sqlalchemy import ModelSchema
from ..model.book_model import Book
from marshmallow import fields, pre_load, ValidationError
from server import db
from server.constant import Constant

from server.utils.bcript_password import Bcript_password


class BookSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Book
        sqla_session = db.session
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    image = fields.String(default="", missing= "")
    author = fields.String(default="", missing= "")
    category = fields.String(default="", missing= "")
    user_id = fields.Integer(required=True)

    created_at = fields.DateTime()
    updated_at = fields.DateTime()

