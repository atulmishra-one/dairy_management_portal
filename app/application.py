"""
This Module is core Application
"""

from importlib import import_module
from flask import Flask

from app.modules import modules


def initialize_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    
    for module in modules:
        import_module(module.import_name)
        app.register_blueprint(module)
    return app
