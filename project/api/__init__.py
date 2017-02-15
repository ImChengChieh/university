#!/user/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

api = Blueprint(__name__, 'api')

from . import article_api,frendshiplink_api,admin_api
