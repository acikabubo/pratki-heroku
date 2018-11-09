from flask_wtf import FlaskForm
from wtforms import (StringField, PasswordField, BooleanField, TextField,
    DateField, SubmitField)
from wtforms.validators import (DataRequired, Length, ValidationError,
    Email, EqualTo)
from flask_uploads import UploadSet, TEXT
from flask_wtf.file import FileField, FileAllowed, FileRequired
from datetime import date, timedelta
from .models import User


txt = UploadSet('txts', TEXT)


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
        render_kw={"placeholder": "Username"})
    email = StringField('Email', validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired()],
        render_kw={"placeholder": "Password"})
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')],
        render_kw={"placeholder": "Repeat password"})
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
        render_kw={"placeholder": "Username"})
    password = PasswordField('Password', validators=[DataRequired()],
        render_kw={"placeholder": "Password"})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField(
        'Password',
        render_kw={"placeholder": "Password"})
    password2 = PasswordField(
        'Repeat Password', validators=[EqualTo('password')],
        render_kw={"placeholder": "Repeat Password"})
    submit = SubmitField('Update')


class UploadForm(FlaskForm):
    file = FileField('File',
        validators=[
            FileRequired(),
            FileAllowed(txt, 'txt only!')
        ],
        render_kw={
            'class': 'form-control'})


class PackageForm(FlaskForm):
    track_no = TextField('Track #',
        validators=[
            DataRequired(),
            Length(min=13, max=16)  # LENGTH VALIDATION DOES NOT WORK
        ],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Enter track #'})
    shipped_on = DateField('Shipped on',
        validators=[DataRequired()],
        render_kw={
            'type': 'text',
            'onfocus': "(this.type='date')",
            'onblur': "if(this.value==''){this.type='text'}",
            'min': date.today() - timedelta(days=30),
            'max': date.today(),
            'class': 'form-control',
            'placeholder': 'Shipped On'})

    name = TextField('Package name',
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Package name/description'})
