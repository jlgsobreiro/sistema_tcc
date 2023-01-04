from flask_wtf import FlaskForm
from wtforms.fields import *


class LoginForm(FlaskForm):
    user = StringField()
    password = PasswordField()

    remember_me = BooleanField()
    submit = SubmitField()


class RegisterForm(FlaskForm):
    usuario = StringField()
    senha = StringField()
    nome = StringField()
    sobrenome = StringField()
    email = EmailField()
    telefone = StringField()

    submit = SubmitField()
