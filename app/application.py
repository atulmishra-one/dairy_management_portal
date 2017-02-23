"""
This Module is core Application
"""

import locale
import logging
from logging.handlers import RotatingFileHandler
from importlib import import_module

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from app.modules import modules
from app.services.extension import login_manager
from app.services.extension import db
from app.services.extension import migrate
from app.services.extension import mail
from app.services.extension import assets
from app.services.session import RedisSessionInterface
from app.config import app_config


def initialize_app(config_object):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_object])

    handler = RotatingFileHandler('application.log')
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    
    for module in modules:
        import_module(module.import_name)
        app.register_blueprint(module)

    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.session_interface = RedisSessionInterface()
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    assets.init_app(app)
    
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    with app.app_context():
        import_module('app.middleware.filters')
        import_module('app.middleware.processor')
        db.create_all()
    
    return app

