from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, SubmitField, BooleanField, PasswordField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from flask_wtf.file import FileField, FileAllowed, FileRequired


class LoginForm(FlaskForm):
    email = StringField('Email ', validators=[Email("Некорректный email")])
    psw = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=100, message='Length of password must be between 4 and 100 symbols')])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    email = StringField('Email: ', validators=[Email("Некорректный email")])
    psw = PasswordField('Password:', validators=[DataRequired(), Length(min=4, max=100, message="Length of password must be between 4 and 100 symbols")])
    psw2 = PasswordField('Repeat password: ', validators=[DataRequired(), EqualTo('psw', message="Passwords don't match")])
    submit = SubmitField('Register')


class UploadForm(FlaskForm):
    image_origin = FileField('image', validators=[FileRequired('File field should not be empty'), FileAllowed(['jpg', 'png'], 'Only images are allowed')])
    select = SelectField(u'Style', choices=[(1, 'Carpet'), (2, 'Vibe-lines'), (3, 'Diamonds')])
    submit = SubmitField('Render')
    recaptcha = RecaptchaField()