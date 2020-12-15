from server import db
from server.constant import Constant

from sqlalchemy.sql import func
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy import text

class User(db.Model):
    """Data model for user accounts."""

    __tablename__ = 'user'
    id = db.Column(
        INTEGER(unsigned=True),
        primary_key=True
    )

    email = db.Column(
        db.String(80),
        index=True,
        unique=True,
        nullable=False
    )

    firstname = db.Column(
        db.String(50),
    )

    lastname = db.Column(
        db.String(50),
    )

    password = db.Column(
        db.String(256),
        nullable=False
    )

    avatar = db.Column(
        db.String(256),
    )

    role = db.Column(
        db.Enum(Constant.ROLE['USER_ROLE']),
        default=Constant.ROLE['USER_ROLE'].user,
        nullable=False
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
    
    def __init__(self, email, firstname, lastname, password, avatar, role):
        self.email = email
        self.firstname = firstname
        self.lastname = lastname
        self.password = password
        self.avatar = avatar
        self.role = role
    def __repr__(self):
        return '' % self.id