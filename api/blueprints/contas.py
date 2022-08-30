import json

from flask import Blueprint, render_template, current_app, Flask, request
from flask_wtf import Form, RecaptchaField, FlaskForm
from flask_wtf.file import FileField
from wtforms import (StringField, HiddenField, ValidationError, RadioField, BooleanField, SubmitField, IntegerField,
                     FormField, validators, FloatField, DateField, Label)
from wtforms.validators import DataRequired, InputRequired

contas = Blueprint('contas', __name__)


class ContasForm(FlaskForm):
    field1 = StringField('Empresa', id='empresa', description='Empresa de cobrança', validators=[InputRequired()])
    label1 = Label('_empresa', 'Empresa')
    field2 = FloatField('Valor', id='valor', description='Valor da conta', validators=[InputRequired()])
    label2 = Label('_valor', 'Valor')
    field3 = DateField('Vencimento', id='vencimento', description='Vencimento da cobrança',
                       validators=[InputRequired()])
    label3 = Label('_vencimento', 'Vencimento')
    field4 = FloatField('Juros', id='juros', description='Valor de juros cobrado', validators=[InputRequired()])
    label4 = Label('_juros', 'Juros')
    field5 = FloatField('Multa', id='multa', description='Valor de multa cobrado', validators=[InputRequired()])
    label5 = Label('_multa', 'Multa')
    field6 = DateField('Emissão', id='emissao', description='Emissão da cobrança', validators=[InputRequired()])
    label6 = Label('_emissao', 'Emissão')


@contas.route('/contas', methods=['POST', 'GET'])
def main():
    return render_template('admin/contas/main.html')


@contas.route('/contas/cadastro', methods=['POST', 'GET'])
def cadastrar():
    form = ContasForm()
    return render_template('admin/contas/cadastro.html', form=form)
