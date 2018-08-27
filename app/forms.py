from flask_wtf import FlaskForm
from wtforms import TextField, DateTimeField
from wtforms.validators import DataRequired, Length
from flask_uploads import UploadSet, TEXT
from flask_wtf.file import FileField, FileAllowed, FileRequired


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
    shipped_on = DateTimeField('Shipped on',
        validators=[DataRequired()],
        render_kw={
            'type': 'date',
            'class': 'form-control',
            'placeholder': 'Shipped On'})

    name = TextField('Package name',
        validators=[DataRequired()],
        render_kw={
            'class': 'form-control',
            'placeholder': 'Package name/description'})
