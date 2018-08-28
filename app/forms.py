from flask_wtf import FlaskForm
from wtforms import TextField, DateField
from wtforms.validators import DataRequired, Length
from flask_uploads import UploadSet, TEXT
from flask_wtf.file import FileField, FileAllowed, FileRequired
from datetime import date, timedelta

txt = UploadSet('txts', TEXT)


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
            'min': date.today()-timedelta(days=30),
            'max': date.today(),
            'class': 'form-control',
            'placeholder': 'Shipped On'})

    name = TextField('Package name',
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Package name/description'})
