from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, Label, FloatField, DateField
from wtforms.validators import InputRequired

from _models.Usuario import Usuario
from dao.usuarios import Usuarios

clientes = Blueprint('clientes', __name__)


class ClientesForm(FlaskForm):
    field1 = StringField('Empresa', id='empresa', description='Empresa de cobrança', validators=[InputRequired()])
    label1 = Label('_empresa', 'Empresa')


@clientes.route('/clientes')
def main():
    _clientes = Usuarios().to_list_of_class_object(where='', class_reference=Usuario)
    return render_template('admin/clientes/main.html', clientes=_clientes)
