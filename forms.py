from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class UserSignUpForm(FlaskForm):
    # email, password, submit, first_name, last_name, username
    email = StringField('Email', validators = [DataRequired(), Email()])
    first_name = StringField('First Name', validators = [DataRequired()])
    last_name = StringField('Last Name', validators = [DataRequired()])
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Create Password', validators = [DataRequired(), Length(min=5, message='5 Characters Required')])
    submit_button = SubmitField()
    
class UserSignInForm(FlaskForm):
    # email, password, submit, first_name, last_name
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Enter Password', validators=[DataRequired()])
    submit_button = SubmitField()
    