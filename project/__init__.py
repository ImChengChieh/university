#!/user/bin/env python
# -*- coding: utf-8 -*-

from config import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_mail import Message,Mail

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
login_manager= LoginManager()
login_manager.session_protection = 'Strong'
login_manager.login_view = 'project.admin.login'
login_manager.login_message = u'请登陆，再访问此页面！'

def create_app(config_name):
    import sys
    if sys.version_info.major < 3:
        reload(sys)
    sys.setdefaultencoding('utf8')

    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    login_manager.init_app(app)

    db.init_app(app)
    db.app = app
    bootstrap.init_app(app)
    moment.init_app(app)
    mail.init_app(app)


    register_blueprints(app)

    add_filter(app)

    return app


def register_blueprints(app):
    from project.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from project.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix="/api")

    from project.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin")


def add_filter(app):
    def exp_replace(arg, regex, newstring=''):
        import re
        str_ = str(arg)
        result, number = re.subn(regex, newstring, arg)
        return result

    app.add_template_filter(exp_replace)
