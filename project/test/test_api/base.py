#!/user/bin/env python
# -*- coding: utf-8 -*-

from flask_testing import TestCase
from project import db
from project import create_app as create_app_


class BaseTestCase(TestCase):
    def create_app(self):
        return create_app_('testing')

    def init_database(self):
        db.create_all()
        from project.models import ArticleType
        ArticleType.init_data()

    def setUp(self):
        self.init_database()

    def tearDown(self):
        db.session.remove()
        db.drop_all()