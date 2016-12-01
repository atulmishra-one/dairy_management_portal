from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class DepartmentForm(FlaskForm):
    department_code = StringField(validators=[DataRequired(), Length(min=2, max=30)])
    department_name = StringField(validators=[DataRequired(), Length(min=2, max=128)])
    department_description = StringField()