"""
Base configuration file

"""

class BaseConfig(object):
    DEBUG = True
    SITE_TITLE = 'Dairy Manager'
    SECRET_KEY = r'\xb4\x0c\x9c\xbdQ\xc0\x81=}\x07\x19j%\xfb\x9a\x8e\x17\x81\\Z\x9c'
    TESTING = True
    DB_USERNAME = ''
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_NAME = ''
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1/dairy_manager' #% (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)
    DATABASE_URI = 'mysql://root:root@127.0.0.1/dairy_manager'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    #MAIL_USE_TLS = False
    MAIL_USERNAME = 'atulmishra.one@gmail.com'
    MAIL_PASSWORD = 'atul123@#'