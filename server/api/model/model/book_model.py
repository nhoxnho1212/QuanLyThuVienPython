from server import db
from server.constant import Constant

from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import text , ForeignKey

class Book(db.Model):
    """Data model for user accounts."""
    __tablename__ = 'book'
    id = db.Column(
        INTEGER(unsigned=True),
        primary_key=True
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    author = db.Column(
        db.String(200),
    )

    category = db.Column(
        db.String(500),
    )

    image = db.Column(
        db.String(256),
        default=''
    )

    user_id = db.Column(
        INTEGER(unsigned=True),
        ForeignKey('user.id')
    )

    created_at = db.Column(
        TIMESTAMP,
        index=False,
        unique=False,
        nullable=False,
        server_default=func.now()
    )

    updated_at = db.Column(
        TIMESTAMP,
        nullable=False,
        server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'), # Use for mysql 5.6.5+
    )

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, name, author, category, image, user_id):
        self.name = name
        self.author = author
        self.category = category
        self.image = image
        self.user_id = user_id

