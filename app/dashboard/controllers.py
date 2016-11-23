"""
This is dashboard module controller
It define dashboard routes
"""

from flask import render_template
from flask import request
from flask import flash
from flask import redirect
from flask import url_for
from flask_login import current_user
from flask_login import login_required

from app.modules import dashboard_module


@dashboard_module.route('', methods=['GET'])
@login_required
def index():
    
    return render_template('dashboard/index.html')