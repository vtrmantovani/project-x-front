import logging
import os


class BaseConfig(object):
    DEBUG = False
    LOGS_LEVEL = logging.INFO
    SQLALCHEMY_DATABASE_URI = os.environ.get('PXF_DB_URI', 'sqlite:///:memory:')  # noqa
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/pxf'
    SECRET_KEY = 'b21032d50cbf2bbfe56a'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = logging.ERROR
