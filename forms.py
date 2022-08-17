from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class LoginForm(FlaskForm):
    email = StringField('Email ', validators=[Email("Некорректный email")])
    psw = PasswordField('Password', validators=[DataRequired(), Length(min=4, max=100, message='Пароль должен быть от 4 до 100 символов')])
    remember = BooleanField('Remember me', default=False)
    submit = SubmitField('Sign in')


class RegisterForm(FlaskForm):
    email = StringField('Email: ', validators=[Email("Некорректный email")])
    psw = PasswordField('Password:', validators=[DataRequired(), Length(min=4, max=100, message='Пароль должен быть от 4 от 100 символов')])
    psw2 = PasswordField('Repeat password: ', validators=[DataRequired(), EqualTo('psw', message='Пароли не совпадают')])
    submit = SubmitField('Register')