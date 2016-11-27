from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class AddRoleForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=2, max=64)])
    allowed_funcs = StringField(validators=[DataRequired()])
    disallowed_funcs = StringField()