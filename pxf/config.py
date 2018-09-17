import logging
import os


class BaseConfig(object):
    DEBUG = False
    LOGS_LEVEL = logging.INFO
    SQLALCHEMY_DATABASE_URI = os.environ.get('PXF_DB_URI', 'sqlite:///:memory:')  # noqa
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY = os.environ.get('SECRET_KEY')

    PXA_URL = os.environ.get('PXA_URL', 'http://127.0.0.1:5000')
    PXA_URL_API_KEY = os.environ.get('PXA_URL_API_KEY', 'test.DU4jJQ.o8vOA378DsITlFQx1etXqt3c-8Q')  # noqa
    PXA_TIMEOUT = int(os.environ.get('PXA_TIMEOUT', 10))


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root@localhost/pxf'
    SECRET_KEY = 'b21032d50cbf2bbfe56a'


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True


class StagingConfig(BaseConfig):
    LOGS_LEVEL = logging.ERROR
    SQLALCHEMY_POOL_SIZE = 50


class ProductionConfig(BaseConfig):
    LOGS_LEVEL = logging.ERROR
    SQLALCHEMY_POOL_SIZE = 50
