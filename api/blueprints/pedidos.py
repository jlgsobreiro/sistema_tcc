from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, Label, FloatField, DateField
from wtforms.validators import InputRequired

pedidos = Blueprint('pedidos', __name__)


class PedidosForm(FlaskForm):
    field1 = StringField('Empresa', id='empresa', description='Empresa de cobrança', validators=[InputRequired()])
    label1 = Label('_empresa', 'Empresa')


@pedidos.route('/pedidos')
def main():
    return render_template('admin/pedidos/main.html')

