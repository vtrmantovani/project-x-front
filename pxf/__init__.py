import logging
import os
import sys
from flask import Flask
from flask_argon2 import Argon2
from flask_bootstrap import Bootstrap
from flask_migrate import Migrate
from flask_principal import Principal
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.exceptions import Forbidden, InternalServerError, NotFound


bootstrap = Bootstrap()

db = SQLAlchemy(session_options={'autoflush': False})

logger = logging.getLogger(__name__)

login_manager = LoginManager()

migrate = Migrate()


def setup_login_manager():
    from pxf.models import User
    login_manager.user_callback = User.load_user
    login_manager.login_view = 'site.login'
    login_manager.login_message = 'Efetue o login para continuar'
    login_manager.login_message_category = 'warning'


def configure_logger(app):
    if not logger.handlers:
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(app.config['LOGS_LEVEL'])
        logger.addHandler(ch)


def create_app(config_var=os.getenv('DEPLOY_ENV', 'Development')):
    # init application
    app = Flask(__name__)
    app.config.from_object('pxf.config.%sConfig' % config_var)

    # configure logger
    configure_logger(app)

    # configure argon2
    app.argon2 = Argon2(app)

    # init bootstrap
    bootstrap.init_app(app)

    # init database
    db.init_app(app)
    _module_dir = os.path.dirname(os.path.abspath(__file__))
    migrate.init_app(app, db, directory=os.path.join(_module_dir, '..', 'migrations'))  # noqa

    # init flask principal
    Principal(app)

    # configure login manager
    login_manager.init_app(app)
    setup_login_manager()

    # register Blueprints
    from pxf.views.common import bp_common
    app.register_blueprint(bp_common)
    from pxf.views.websites import bp_websites
    app.register_blueprint(bp_websites)
    from pxf.views.site import bp_site, forbidden, internal_server_error, not_found  # noqa
    app.register_blueprint(bp_site)
    app.register_error_handler(Forbidden.code, forbidden)
    app.register_error_handler(InternalServerError.code, internal_server_error)
    app.register_error_handler(NotFound.code, not_found)

    return app
