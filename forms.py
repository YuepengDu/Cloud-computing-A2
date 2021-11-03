from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileField, FileAllowed, FileRequired

class RegistrationForm(FlaskForm):
    email = EmailField('Email',
                        validators=[DataRequired(), Email()])
    user_name = StringField('Name',
                           validators=[DataRequired(), Length(min=1, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = EmailField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SearchForm(FlaskForm):
    title = StringField()
    artist = StringField()
    year = StringField()
    submit = SubmitField('Query')