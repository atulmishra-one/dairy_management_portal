from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask import make_response
from flask import jsonify
from flask_login import current_user

from app.modules import departments_module
from .models.departments import Department
from .forms import DepartmentForm
from app.services.extension import sqlalchemy as db


@departments_module.route('')
def index():
    departments = Department.query.all()
    form = DepartmentForm(request.form)
    
    return render_template(
        'departments/index.html',
        departments=departments,
        form=form
    )


@departments_module.route('/create', methods=['POST', ])
def create():
    form = DepartmentForm(request.form)
    
    if form.validate_on_submit():
        try:
            department = Department.query.filter(Department.department_name==form.department_name.data).first()
            if not department:
                db.session.add(Department(
                    department_code=form.department_code.data,
                    department_name=form.department_name.data,
                    department_description=form.department_description.data
                ))
            else:
                department.department_code=form.department_code.data
                department.department_name=form.department_name.data
                department.department_description=form.department_description.data
                db.session.add(department)
                    
            db.session.commit()
            return jsonify(success='Department Information saved successfully.')
        except Exception as e:
            return make_response(jsonify(error='An error occurred try again later.'), 500)
    else:
        return make_response(jsonify(form.errors), 500) 
    return ''

