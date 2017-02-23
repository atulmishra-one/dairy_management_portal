"""
This Modules is core part of Dairy Manager
"""

from flask import Blueprint
from werkzeug.security import generate_password_hash


def include(module_name, url_prefix, template_folder='templates', static_folder='static'):
    name = module_name
    import_name = 'app.{}'.format(name)
    module_name = Blueprint(
        name,
        import_name,
        template_folder=template_folder,
        static_folder=static_folder,
        url_prefix=url_prefix
    )
    return module_name


class UserPasswordGenerator(object):
    def __init__(self, password):
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

