#!/user/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint
from ..models import Permission
admin = Blueprint(__name__, 'admin')


from . import views,adminlogin,verify_views,news_views,institutional_views,photo_video_views


#把Permissions加入模板上下文
@admin.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)