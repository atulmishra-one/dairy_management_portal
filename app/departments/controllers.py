from flask import render_template
from flask import request
from flask import make_response
from flask import jsonify

from app.modules import department_module
from app.departments.forms import DepartmentForm
from app.departments.models.department import Department
from app.users.models.user import User
from app.roles.models.role import Role
from app.services.extension import db


@department_module.route('')
def index():
    form = DepartmentForm(request.form)

    departments = Department.query.all()
    users = User.query.all()
    roles = Role.query.all()

    return render_template(
        'departments/index.html',
        form=form,
        departments=departments,
        users=users,
        roles=roles
    )


@department_module.route('/add', methods=['POST'])
def add():
    form = DepartmentForm(request.form)

    if form.validate_on_submit():
        department = Department(
            name=form.name.data,
            active=1,
            description=''
        )
        db.session.add(department)
        db.session.commit()

        roles = request.form.getlist('roles[]')
        for role in roles:
            db.session.execute("""
            INSERT INTO department_roles SET department_id=%s, role_id=%s
            """ % (department.id, role))

        users = request.form.getlist('users[]')
        for user in users:
            db.session.execute("""
                        UPDATE user SET department_id=%s WHERE id=%s
                        """ % (department.id, user))
        db.session.commit()

        return jsonify(success='Department Information recorded successfully.')
    else:
        return make_response(jsonify(form.errors), 500)

