from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import BooleanField
from wtforms import IntegerField
from wtforms.validators import DataRequired
from wtforms.validators import Length

class UserForm(FlaskForm):
    initial_name = StringField()
    first_name = StringField(validators=[DataRequired(), Length(min=2, max=64)])
    last_name = StringField(validators=[DataRequired(), Length(min=2, max=64)])
    username = StringField(validators=[DataRequired(), Length(min=2, max=64)])
    password = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired()])
    active = BooleanField()
    role_id = IntegerField()

    
class SendEmailForm(FlaskForm):
    to = StringField(validators=[DataRequired()])
    subject = StringField(validators=[DataRequired()])
    message = StringField(validators=[DataRequired()])