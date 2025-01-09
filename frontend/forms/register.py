from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField,PasswordField
from wtforms.validators import DataRequired,EqualTo,Email

class RegisterForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Continue')