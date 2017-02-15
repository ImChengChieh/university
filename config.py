#!/user/bin/env python
# -*- coding: utf-8 -*-
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__name__))


# os.urandom(24) gegnerate random string
class Config(object):
    SECRET_KEY = '\xa0\xc8<{\xa6ZL\xe9\xc2\xc7\x88\xbeM)\x9cpH\xf3^\xdf\xa4\x87\xb3\xcd'
    ARTICLE_LIST_LEN = 5  # 文章列表
    ADMIN_LIST_ADMIN = 10  # 管理员列表
    ADMIN_LIST_LOG = 20  # 日志列表
    ARTICLE_LIST_ADMIN = 11  # 管理员页面文章列表
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False

    RECOMMEND_ARTICLES_LEN = 15

    FLASK_ALUMNIS_PER_PAGE = 15

    FLASY_BANNER_PER_PAGE = 15
    FLASY_NEWS_PER_PAGE = 15
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    # SQL CONFIG
    # SQL statement:
    #   CREATE DATABASE IF NOT EXISTS college_dev DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
    #   GRANT ALL PRIVILEGES ON ktest.* TO 'uniyes'@'localhost' IDENTIFIED BY 'uniyes123' WITH GRANT OPTION;
    # SQLALCHEMY_DATABASE_URI = 'mysql://uniyes:uniyes123@127.0.0.1/college_dev?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = 'mysql://college:uniyes123@118.178.233.23:3306/college'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/college'
    # SQLALCHEMY_DATABASE_URI = 'mysql://uniyes:uniyes123@127.0.0.1/college_dev?charset=utf8'
    SQLALCHEMY_DATABASE_URI = 'mysql://college:uniyes123@118.178.233.23:3306/college?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@localhost/college'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/college'
    # SQLALCHEMY_DATABASE_URI = 'mysql://uniyes:uniyes123@127.0.0.1/college_dev?charset=utf8'
    SQLALCHEMY_ECHO = True
    DEBUG = True

    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '2476159529'
    MAIL_PASSWORD = 'nzowhnltpfdiebjd'




class IntegrationConfig(DevelopmentConfig):
    pass


class TestingConfig(Config):
    # SQL CONFIG
    # SQL statement:
    #   CREATE DATABASE IF NOT EXISTS ktest DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
    #   GRANT ALL PRIVILEGES ON ktest.* TO 'uniyes'@'localhost' IDENTIFIED BY 'uniyes123' WITH GRANT OPTION;
    # SQLALCHEMY_DATABASE_URI = 'mysql://uniyes:uniyes123@127.0.0.1/college_dev?charset=utf8'
    # SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/college'

    TESTING = True


class IntegrationTestingConfig(TestingConfig):
    pass


class ProductionConfig(Config):
    pass


config = {
    'development': DevelopmentConfig,
    'integration': IntegrationConfig,
    'testing': TestingConfig,
    'integration_testing': IntegrationTestingConfig,
    'production': ProductionConfig
}
