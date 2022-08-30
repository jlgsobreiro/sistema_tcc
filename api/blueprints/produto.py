import uuid

import flask_login
from flask import Blueprint, request, flash, redirect, render_template, url_for
from _models.Produto import Produto
from dao.estoque import Estoque, EstoqueDAO
from dao.produtodao import ProdutoDAO
from flask_wtf import FlaskForm
from wtforms import StringField, Label, FloatField, DateField, DecimalField, IntegerField, SelectField, BooleanField
from wtforms.validators import InputRequired

produto = Blueprint('produto', __name__)


class ProdutosForm(FlaskForm):
    nome = StringField('Nome', id='nome', description='Nome do produto', validators=[InputRequired()])
    label_nome = Label('nome', 'Nome')
    valor = DecimalField('Valor', id='valor', description='Valor de venda', validators=[InputRequired()])
    label_valor = Label('valor', 'Valor')
    custo = DecimalField('Custo', id='custo', description='Valor pago pelo cujo', validators=[InputRequired()])
    label_custo = Label('custo', 'Custo')
    codigo_de_barras = IntegerField('Codigo de Barras', id='codigo_de_barras', description='Codigo de leitura',
                                    validators=[InputRequired()])
    label_codigo_de_barras = Label('codigo_de_barras', 'Codigo de Barras')
    origem = StringField('Origem', id='origem', description='Origem', validators=[InputRequired()])
    label_origem = Label('origem', 'Origem')
    unidade = SelectField('Unidade', choices=['KG', 'G', 'UN', 'L'], id='unidade', description='Unidade',
                          validators=[InputRequired()])
    label_unidade = Label('unidade', 'Unidade')
    condicao = BooleanField('Codição', id='condicao', description='Disponível para venda')
    label_condicao = Label('condicao', 'Condição')
    insumo = BooleanField('Insumo', id='insumo', description='Pode ser usado como material')
    label_insumo = Label('insumo', 'Insumo')
    quantidade = IntegerField('Quantidade', id='quantidade', description='Unidades em estoque',
                              validators=[InputRequired()])
    label_quantidade = Label('quantidade', 'Quantidade')


@produto.route('/produto')
def main():
    inventory = ProdutoDAO().to_list_of_class_object(where='', class_reference=Produto)
    return render_template('admin/produtos/main.html', inventory=inventory)


@produto.route('/produto/<_product_id>')
def produto_id(_product_id):
    return render_template('admin/produtos/product.html')


@produto.route('/produto/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    form = ProdutosForm()
    if request.method == 'POST':
        product_obj = Produto().from_dict(request.form)
        product_id = str(uuid.uuid4())
        product_obj._id = product_id
        res = ProdutoDAO().register(product_obj)
        if res.get('error') is None:
            flash('foi', 'success')
            res2 = EstoqueDAO().register(
                Estoque(produto_id=product_id, loja_id=0, quantidade=request.form.get('quantidade')))
            return redirect(url_for('admin.adm_home'))
        else:
            flash(res.get('error'), 'error')
    return render_template('admin/produtos/produto_cadastro.html', form=form)


@produto.route('/produto/<_product_id>/editar', methods=['GET', 'POST', 'DELETE'])
def editar_produto(_product_id):
    form = ProdutosForm()
    product_obj = ProdutoDAO().to_class_object(f"_id = '{_product_id}'", Produto)
    form.nome.data = product_obj.nome
    form.valor.data = product_obj.valor
    form.custo.data = product_obj.custo
    form.codigo_de_barras.data = product_obj.codigo_de_barras
    form.unidade.data = product_obj.unidade
    form.origem.data = product_obj.origem
    form.condicao.data = product_obj.active
    if request.method == 'POST':
        if request.form.get('save'):
            product_obj = Produto().from_dict(request.form)
            product_obj.__setattr__('_id', _product_id)
            res = ProdutoDAO().update(where=f"_id = '{_product_id}'",
                                      updated_object=product_obj,
                                      class_reference=Produto)
            if res.get('error') is None:
                res2 = EstoqueDAO().update(where=f"produto_id = '{_product_id}'",
                                           updated_object=Estoque(produto_id=product_obj.get_id(), loja_id=0,
                                                                  quantidade=0)
                                           , class_reference=Estoque)
            if res.get('error'):
                flash(res.get('error'), 'error')
            else:
                flash(res.get('success'), 'success')
        elif request.form.get('delete'):
            res = ProdutoDAO().delete(f"_id = '{_product_id}'")
            if res.get('error') is None:
                res = EstoqueDAO().delete(f"produto_id = '{_product_id}'")
                if res.get('error') is None:
                    flash(res, 'success')
                else:
                    flash(res, 'error')
            else:
                flash(res, 'error')
            return redirect(url_for('main'))
    return render_template('admin/produtos/produto_editar.html', _product_id=_product_id, form=form)
