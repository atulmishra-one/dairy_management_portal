"""
This is default module controller
"""

from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user

from app.modules import default_module
from app.default.forms import LoginForm
from app.services.extension import login_manager
from app.services.extension import db
from app.users.models.user import User


@login_manager.user_loader
def load_user(id):
    return User.query.filter(User.id == id, User.active == 1).first()


@default_module.route('/', methods=['GET', 'POST', ])
def index():
    form = LoginForm(request.form)
    
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.controllers.index'))
    
    if request.method == 'POST':
        if form.validate_on_submit():
            user = User.query.filter_by(
                username=form.username.data,
                password=form.password.data
            ).first()
            if user and user.active:
                user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('dashboard.controllers.index'))
            else:
                form.username.errors.append('Invalid Username/Password.')
                flash(form.errors)
                return redirect(url_for('default.controllers.index'))
        else:
            flash(form.errors)
            return redirect(url_for('default.controllers.index'))
        
    return render_template('default/index.html', form=form)


@default_module.route('logout')
def logout():
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return redirect(url_for('default.controllers.index'))

