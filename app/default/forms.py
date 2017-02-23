from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired(), Length(min=2, max=64)])
    password = StringField(validators=[DataRequired()])

