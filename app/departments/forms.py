from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class DepartmentForm(FlaskForm):
    name = StringField(validators=[DataRequired(), Length(min=2, max=64)])
    active = BooleanField()
    description = StringField()

