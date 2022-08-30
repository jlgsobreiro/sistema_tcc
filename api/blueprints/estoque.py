from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, Label, FloatField, DateField
from wtforms.validators import InputRequired

estoque = Blueprint('estoque', __name__)


class EstoqueForm(FlaskForm):
    field1 = StringField('Empresa', id='empresa', description='Empresa de cobrança', validators=[InputRequired()])
    label1 = Label('_empresa', 'Empresa')


@estoque.route('/estoque')
def main():
    return render_template('admin/estoque/main.html')
