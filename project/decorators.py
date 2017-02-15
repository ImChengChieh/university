# coding:utf-8
from functools import wraps
from flask import abort
from flask_login import current_user
from models import Permission


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)

        return decorated_function

    return decorator


def admin_required(f):  # 管理员权限
    return permission_required(Permission.ADMINISTER)(f)


def modify_required(f):  # 添加文章权限
    return permission_required(Permission.WRITE_ARTICLES)(f)
