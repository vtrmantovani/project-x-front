import logging
import os
import sys
from flask import Flask

logger = logging.getLogger(__name__)


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

    # register Blueprints
    from pxf.views.common import bp_common
    app.register_blueprint(bp_common)

    return app
