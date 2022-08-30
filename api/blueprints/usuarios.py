from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, Label, FloatField, DateField
from wtforms.validators import InputRequired

usuarios = Blueprint('usuarios', __name__)


class UsuariosForm(FlaskForm):
    field1 = StringField('Empresa', id='empresa', description='Empresa de cobrança', validators=[InputRequired()])
    label1 = Label('_empresa', 'Empresa')


@usuarios.route('/usuarios')
def main():
    return render_template('admin/usuarios/main.html')
