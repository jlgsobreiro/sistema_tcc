from flask import Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, Label, FloatField, DateField
from wtforms.validators import InputRequired

insumos = Blueprint('insumos', __name__)


class InsumosForm(FlaskForm):
    field1 = StringField('Empresa', id='empresa', description='Empresa de cobrança', validators=[InputRequired()])
    label1 = Label('_empresa', 'Empresa')



@insumos.route('/insumos')
def main():
    return render_template('admin/insumos/main.html')
