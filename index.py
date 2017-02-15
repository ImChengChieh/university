#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
BAE start file
"""
from run import app
from bae.core.wsgi import WSGIApplication

application = WSGIApplication(app)