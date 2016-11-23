from flask import render_template
from flask import current_app
from flask import url_for

from app.modules import roles_module
from .utils import user_functions
from app.models.core.role import Role


@roles_module.route('')
def index():
    functions = user_functions()
    roles = Role.query.all()
    
    return render_template('roles/index.html', functions=functions, roles=roles)