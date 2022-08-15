import datetime

import flask_login
from flask import Blueprint, request, flash, redirect, url_for, render_template
from flask_login import login_user

from _models.Estoque import Estoque
from _models.Produto import Produto
from _models.Lojas import Lojas
from _models.ShopAdmin import ShopAdmin
from _models.Usuario import Usuario
from dao.estoque import Estoque
from dao.produtos import Products
from dao.shop_admins import ShopAdmins
from dao.lojas import Lojas
from dao.usuarios import Usuarios

produto = Blueprint('produto', __name__)


@produto.route('/produto')
def main():
    return render_template('admin/produtos/main.html')

@produto.route('/produto/<_product_id>')
def shop_product_id(_product_id):
    return render_template('admin/produtos/product.html')


@produto.route('/produto/<_product_id>/editar', methods=['GET', 'POST'])
def edit_shop_product(_product_id):
    _product_id = request.form.get('product_id')
    _id = request.form.get('shop_id')
    _id = 0
    product_obj = Products().to_class_object(f'_id = {_product_id}', Produto) if _product_id != 'new' else Produto()
    if request.method == 'POST':
        if request.form.get('save'):
            if _product_id == 'new':
                product_obj = Produto().from_dict(request.form)
                product_id = Products().get_count('') + 1 if product_obj.get_id() == '' else product_obj.get_id()
                product_obj._id = product_id
                res = Products().register(product_obj)
                if res.get('error') is None:
                    res2 = Estoque().register(Estoque(product_id=product_id, shop_id=0, quantity=0))
            else:
                product_obj = Produto().from_dict(request.form)
                res = Products().update(where=f"_id = '{_product_id}'",
                                        updated_object=product_obj,
                                        class_reference=Produto)
                if res.get('error') is None:
                    res2 = Estoque().update(where=f"product_id = '{_product_id}'",
                                            updated_object=Estoque(product_id=product_obj.get_id(), shop_id=_id,
                                                                   quantity=0),
                                            class_reference=Estoque)
            if res.get('error'):
                flash(res.get('error'), 'error')
            else:
                flash(res.get('success'), 'success')
                return redirect(f"/shop/{_id}/product/{product_obj.get_id()}/edit")
        elif request.form.get('delete'):
            res = Products().delete(f"_id = '{_product_id}'")
            if res.get('error') is None:
                res = Estoque().delete(f"product_id = '{_product_id}' AND shop_id = '{_id}'")
                if res.get('error') is None:
                    flash(res, 'success')
                else:
                    flash(res, 'error')
            else:
                flash(res, 'error')
            return redirect(f'/shop/{_id}/inventory')
    return render_template('admin/produtos/product_edit.html', product=product_obj, shop=shop)
