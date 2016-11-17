"""
Base configuration file

"""

class BaseConfig(object):
    DEBUG = True
    SECRET_KEY = r'\xb4\x0c\x9c\xbdQ\xc0\x81=}\x07\x19j%\xfb\x9a\x8e\x17\x81\\Z\x9c'
    TESTING = True
    DB_USERNAME = ''
    DB_PASSWORD = ''
    DB_HOST = ''
    DB_NAME = ''
    DATABASE_URI = 'mysql://%s:%s@%s/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME)