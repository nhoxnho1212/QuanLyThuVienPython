from enum import Enum
from server.utils.util import enum


class Constant:
    ROLE = {
        'USER_ROLE': Enum(
            value='USER_ROLE',
            names=[
                ('NHAN_VIEN', 'NHAN_VIEN'),
                ('MANAGER', 'MANAGER'),
                ('admin_root', 'admin_root'),
            ]
        )
    }

    FUNCTIONS = {
        'EMPLOYEE': Enum(
            value='EMPLOYEE',
            names=[
                ('THU_THU', 'THU_THU'),
                ('THU_KHO', 'THU_KHO'),
                ('THU_QUY', 'THU_QUY'),
                ('NONE_FUNCTION', 'NONE_FUNCTION')
            ]
        )
    }

    class STATUS_CODE(Enum):
        OK = 200
        CREATED = 201
        NO_CONTENT = 204
        BAD_REQUEST = 400
        UNAUTHORIZED = 401
        FORBIDDEN = 403
        NOT_FOUND = 404
        INTERNAL_SERVER_ERROR = 500
