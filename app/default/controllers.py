"""
This is default module controller
It define default routes
"""

from app.modules import default_module


@default_module.route('')
def index():
    return 'Hello'