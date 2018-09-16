#!/usr/bin/env python
from flask_script import Manager

from pxf import create_app, db
from pxf.models.user import User

app = create_app()

manager = Manager(app)


@manager.option('-p', dest='password', help='User password', required=True)
@manager.option('-e', dest='email', help='User email', required=True)
def create_user(email, password):
    user = User(email=email, password=password)
    user.enabled = True
    db.session.add(user)
    db.session.commit()
    print('User {} created'.format(email))


if __name__ == '__main__':
    manager.run()
