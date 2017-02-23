from flask import render_template
from flask import current_app
from flask import url_for
from flask import make_response
from flask import jsonify
from flask import request
from flask_login import login_required

from app.modules import roles_module
from app.roles.models.role import Role
from app.users.models.user import User
from app.services.extension import db

from .utils import application_functions
from .forms import AddRoleForm
from .forms import DeleteRoleForm
from .utils import permission_required


@roles_module.route('')
@roles_module.route('/<name>')
@login_required
@permission_required
def index(name=None):
    functions = application_functions()
    roles = Role.query.all()
    users = User.query.all()
    
    form = AddRoleForm(request.form)
    
    if name:
        try:
            roles = Role.query.filter(Role.name == name).all()
            roles = [{'allowed_funcs': role.allowed_funcs.split(','), 'disallowed_funcs': role.allowed_funcs.split(',')}
                     for role in roles]
        except AttributeError:
            roles = []
        
        try:
            users = User.query.join(Role).add_columns(User.username).filter(Role.name == name).all()
            users = [{'username': user.username} for user in users]
        except AttributeError:
            users = []
        
        return jsonify(results=roles, users=users)
    
    return render_template('roles/index.html', functions=functions, roles=roles, form=form, users=users)


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
        users = request.form.get('users', type=str).split(',')
        
        
        if created:
            return jsonify(success='Role Information recorded successfully.')
        else:
            return make_response(jsonify(error='An error occurred ! try again later.'), 500)
    else:
        return make_response(jsonify(form.errors), 500)
    return ''


@roles_module.route('/delete', methods=['POST', ])
@login_required
@permission_required
def delete():
    form = DeleteRoleForm(request.form)
    
    if form.validate_on_submit():
        
        deleted = Role.query.filter(Role.name==form.name.data).delete()
        
        if deleted:
            db.session.commit()
            return jsonify(success='Role Information deleted successfully.')
        else:
            return make_response(jsonify(error='An error occurred ! try again later.'), 500)
    else:
        return make_response(jsonify(form.errors), 500)
    return ''
