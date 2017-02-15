#!/user/bin/env python
# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint(__name__, 'main')
# main = Blueprint('main',__name__)

from . import views,news,activity,photo_video
