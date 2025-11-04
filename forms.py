from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp

class StudentForm(FlaskForm):
    firstname = StringField('First Name', validators=[
        DataRequired(), Length(min=1, max=50),
        Regexp(r'^[A-Za-z\s\-]+$', message="Names must contain only letters, spaces or hyphens")])
    lastname = StringField('Last Name', validators=[
        DataRequired(), Length(min=1, max=50),
        Regexp(r'^[A-Za-z\s\-]+$', message="Names must contain only letters, spaces or hyphens")])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone', validators=[
        DataRequired(), Regexp(r'^[0-9+\-\s]{7,20}$', message='Invalid phone')])
    submit = SubmitField('Submit')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('Login')
