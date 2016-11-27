from decorator import decorator
from flask import render_template
from flask import current_app
from flask import url_for
from flask import redirect
from flask_login import current_user

from app.models.core.role import Role
from app.models.core.user import User
from app.services.extension import sqlalchemy as db


def user_functions():
    for rule in current_app.url_map.iter_rules():
        if not ( rule.endpoint.endswith('static') or rule.endpoint.endswith('logout') ) :
            yield "{:50s}".format(rule.endpoint)


@decorator
def permission_required(f, *args, **kwargs):
    try:
        user_id = current_user.id
        allowed_funcs = Role.query.join(User).add_columns(
            Role.allowed_funcs
        ).filter(Role.id==User.role_id, User.id==user_id).all()

        results = [ allowed_func.allowed_funcs.split(',') for allowed_func in allowed_funcs][0]
        
        function_name = "{0}.{1}".format(f.__module__.replace('app.', ''), f.__name__)
        
        if function_name not in results:
            return render_template('roles/permission_denied.html')
        
    except (IndexError, AttributeError):
        return render_template('roles/permission_denied.html')
    return f(*args, **kwargs)
    