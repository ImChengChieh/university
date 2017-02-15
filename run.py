#!/user/bin/env python
# -*- coding: utf-8 -*-

import os
from project import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_script import Server
from project.models import Role, ArticleType, init_dates


config_name = os.getenv('UNIYES_CONFIG') or 'integration'

print("Note:")
print("Current app config name is:", config_name)
print("Note:")
print("If you change system envrionment variables in PyCharm, you need to restart it to reload new settings.")

app = create_app(config_name)
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    # from project.models import init_dates
    # return dict(app=app, db=db, init_dates=init_dates)
    return dict(app=app, db=db)


manager.add_command('runserver', Server(host='localhost', port=9090))
manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)


@manager.command
def init_db():
    Role.insert_roles()
    ArticleType.init_data()
    init_dates()

if __name__ == '__main__':
    manager.run()
