"""
This Module is core Application
"""
import locale
from importlib import import_module
import os

from flask import Flask
from flask_assets import Environment, Bundle

from app.modules import modules
from app.services.extension import login_manager
from app.services.extension import sqlalchemy
from app.services.extension import migrate
from app.services.extension import mail
from app.services.session import RedisSessionInterface


def initialize_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    for module in modules:
        import_module(module.import_name)
        app.register_blueprint(module)
    
    assets = Environment(app)
    js = Bundle('js/jquery-3.1.1.min.js', 'js/bootstrap.min.js')
    css = Bundle('css/bootstrap.min.css', 'css/style.css')
    
    assets.register('js_all', js)
    assets.register('css_all', css)
    
    app.session_interface = RedisSessionInterface()
    
    sqlalchemy.init_app(app)
        
    login_manager.init_app(app)
    migrate.init_app(app, sqlalchemy)
    mail.init_app(app)
    
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
    with app.app_context():
        import_module('app.middleware.filters')
        sqlalchemy.create_all()
    
    return app
