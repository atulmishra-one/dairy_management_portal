"""
This is dashboard module controller
It define dashboard routes
"""
import os

from flask import render_template
from flask import request
from flask import current_app
from flask import flash
from flask import redirect
from flask import url_for
from flask import make_response
from flask import jsonify
from flask import send_file
from flask_login import current_user
from flask_login import login_required
import flask_excel as excel
from flask_mail import Message
from celery.task.control import revoke
from werkzeug.utils import secure_filename

from app.modules import users_module
from app.users.models.user import User
from app.core import UserPasswordGenerator
from .forms import UserForm
from .forms import SendEmailForm
from .tasks import upload_users
from app.services.extension import task_server
from app.services.extension import mail
from app.roles.utils import permission_required
from app.roles.models.role import Role


@users_module.route('/page/<page>', methods=['GET'])
@users_module.route('', methods=['GET'])
@login_required
@permission_required
def index(page=0):

    page = int(page) or 1

    # users = User.query.join(Role).\
    # add_columns(
    #     Role.name,
    #     User.username,
    #     User.initial_name,
    #     User.first_name,
    #     User.last_name,
    #     User.email,
    #     User.active
    # ).\
    # filter(User.role_id==Role.id).\
    # paginate(page, 10, False)

    users  = User.query.paginate(page, 10, False)
    return render_template(
        'users/index.html',
        users=users
    )


@users_module.route('/manage', methods=['GET', 'POST'])
@users_module.route('/manage/<username>', methods=['GET', 'POST'])
@login_required
@permission_required
def manage(username=None):
    roles = Role.query.all()
    form = UserForm(request.form)

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User()
            data = {
                'email': form.email.data,
                'username': form.username.data,
                'password': form.password.data,
                'initial_name': form.initial_name.data,
                'first_name': form.first_name.data,
                'last_name': form.last_name.data,
                'active': form.active.data,
                'role_id': form.role_id.data
            }

            user.create_or_update([data])
            return jsonify(success='User Information recorded successfully.')
        else:
            return make_response(jsonify(form.errors), 500)

    return render_template('users/manage.html', roles=roles, form=form, username=username)


@users_module.route('/search', methods=['GET', 'POST'])
@permission_required
def search():
    q = request.args.get('q', type=str)

    if q:
        users = User.query.filter((User.first_name.ilike('%'+q+'%')) | (User.email.ilike('%'+q+'%'))).all()
        users_list = [
            {
                'id': user.id,
                'initial_name': user.initial_name,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'fullname': "%s %s %s" % (user.initial_name, user.first_name, user.last_name),
                'email': user.email,
                'username': user.username,
                'role_id': 0,
                'active': user.active,
                'password': user.password,
                'authenticated': user.authenticated,
                'department_id': user.department_id
            } for user in users]
        return jsonify(results=users_list)


@users_module.route('/delete', methods=['POST'])
@login_required
@permission_required
def delete():
    if request.method == 'POST':
        username = request.form['username']
        user = User()
        deleted = user.delete_user(username)
        if deleted:
            return jsonify(success='User deleted successfully.')
        else:
            return make_response(jsonify(error='An error occurred ! try again later.'), 500)
    return ''


@users_module.route('/import_users', methods=['GET','POST'])
@login_required
@permission_required
def import_users():

    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)

        upload_path = '/tmp/'
        file_path = upload_path+filename
        try:
            file.save(file_path)
            result = upload_users.delay(file_path)
            flash('Upload Task Started. You will be notified. You can now close this window. ')
            return redirect(url_for('users.controllers.import_users', task_id=result.task_id))
        except IOError:
            flash('You need a Excel file to upload.')
            return redirect(url_for('users.controllers.import_users'))
    else:
        task_id = request.args.get('task_id', type=str)

        if task_id:
            task_status = upload_users.AsyncResult(task_id).status
            if task_status == 'SUCCESS':
                revoke(task_id, terminate=True)
            else:
                return str(task_status)

    return render_template('users/import.html', task_id=task_id)


@users_module.route('/export', methods=['GET','POST'])
@login_required
@permission_required
def export():
    users = User.query.filter(User.username != 'admin' ).all()
    column_names = ['initial_name', 'first_name', 'last_name', 'username', 'email', 'password', 'active']
    return excel.make_response_from_query_sets(users, column_names, "xls", file_name="users.xls")


@users_module.route('/validate_email', methods=['GET', 'POST'])
@login_required
def validate_email():
    """
    Validates user email Address
    """
    email = request.args.get('email')

    if email.find('@') > 1:
        user = User.query.filter_by(email=email).first()
        if user:
            return make_response(jsonify(result='Email exists.'), 500)
        else:
            return make_response(jsonify(result=email), 200)


@users_module.route('/generate_password', methods=['GET', 'POST'])
@login_required
def generate_password():
    username = request.args.get('username')
    password = UserPasswordGenerator(username)

    random_password = password.pw_hash[-5:]

    return jsonify(result=str(unicode(random_password)))


@users_module.route('/send_email', methods=['POST'])
@login_required
@permission_required
def send_email():
    form = SendEmailForm(request.form)

    if form.validate_on_submit():
        msg = Message(form.subject.data, sender='atulmishra.one@gmail.com', recipients=[form.to.data])
        msg.html = render_template('users/email.html', to=form.to.data, subject=form.data.subject, message=form.message.data)
        mail.send(msg)
    flash('Email was sent successfully.', 'success')
    return redirect(url_for('users.controllers.manage'))


