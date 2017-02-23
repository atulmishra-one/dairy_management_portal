"""
Base configuration file

"""

from datetime import datetime


class BaseConfig(object):
    DEBUG = True
    SITE_TITLE = 'Dairy Manager'
    SECRET_KEY = r'\xb4\x0c\x9c\xbdQ\xc0\x81=}\x07\x19j%\xfb\x9a\x8e\x17\x81\\Z\x9c'
    SQLALCHEMY_POOL_SIZE = 5
    SQLALCHEMY_POOL_TIMEOUT = 120
    SQLALCHEMY_POOL_RECYCLE = 280
    TESTING = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    ASSETS_DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
    COPY_RIGHT = 'Copyright &copy; %s. All rights reserved !' % datetime.today().strftime('%Y')


