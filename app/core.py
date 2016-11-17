"""
This Modules is core part of Dairy Manager
"""

from flask import Blueprint

def include(module_name, url_prefix, template_folder=None, static_folder=None):
    name = module_name
    import_name = 'app.{}'.format(name)
    module_name = Blueprint(name, import_name, template_folder=template_folder, static_folder=static_folder, url_prefix=url_prefix)
    return module_name