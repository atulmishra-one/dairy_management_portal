from flask import render_template
from flask import current_app
from flask import url_for
from flask import make_response
from flask import jsonify
from flask import request
from flask_login import login_required

from app.modules import roles_module
from app.models.core.role import Role

from .utils import user_functions
from .forms import AddRoleForm
from .utils import permission_required


@roles_module.route('')
@roles_module.route('/<name>')
@login_required
@permission_required
def index(name=None):
    functions = user_functions()
    roles = Role.query.all()
    
    form = AddRoleForm(request.form)
    
    if name:
        try:
            roles = Role.query.filter(Role.name==name).all()
            roles = [{'allowed_funcs': role.allowed_funcs.split(','), 'disallowed_funcs': role.allowed_funcs.split(',')} for role in roles]
            return jsonify(results=roles)
        except AttributeError:
            return jsonify(results=[])
    
    return render_template('roles/index.html', functions=functions, roles=roles, form=form)


@roles_module.route('/add', methods=['POST', ])
@login_required
@permission_required
def add():
    form = AddRoleForm(request.form)
    
    if form.validate_on_submit():
        created = Role.create_or_update(
            form.name.data, 
            form.allowed_funcs.data, 
            form.disallowed_funcs.data
        )
        if created:
            return jsonify(success='Role Information recorded successfully.')
        else:
            return make_response(jsonify(error='An error occurred ! try again later.'), 500)
    else:
        return make_response(jsonify(form.errors), 500)
    return ''
