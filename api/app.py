import datetime

import flask_login
from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, login_required
from flask_toastr import Toastr

from _models.Estoque import Estoque
from _models.Produto import Produto
from _models.Lojas import Lojas
from _models.ShopAdmin import ShopAdmin
from _models.Usuario import Usuario
from blueprints.clientes import clientes
from blueprints.contas import contas
from blueprints.estoque import estoque
from blueprints.insumos import insumos
from blueprints.pedidos import pedidos
from blueprints.produto import produto
from blueprints.administrador import admin
from blueprints.api import api
from blueprints.usuarios import usuarios
from dao.administradores import Administradores
from dao.estoque import Estoque, EstoqueDAO
from dao.produtodao import ProdutoDAO
from dao.shop_admins import ShopAdmins
from dao.lojas import Lojas
from dao.usuarios import Usuarios
from flask_material import Material

app = Flask(__name__)
app.config.from_pyfile("instance/config.py")
app.register_blueprint(admin)
app.register_blueprint(api)
app.register_blueprint(produto)
app.register_blueprint(clientes)
app.register_blueprint(contas)
app.register_blueprint(estoque)
app.register_blueprint(insumos)
app.register_blueprint(pedidos)
app.register_blueprint(usuarios)
bootstrap = Bootstrap5(app)
toastr = Toastr(app)
Material(app)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    user = Usuarios().get_user_by_id(user_id=user_id)
    if user is None:
        return None
    return user if user_id == user.get_id() else None


@app.route('/', methods=['GET', 'POST'])
def root():
    current_user = flask_login.current_user
    products = ProdutoDAO().to_list_of_class_object('', Produto)[:10]
    products = [ProdutoDAO().to_class_object(f"_id = '{prod.get_id()}'", Produto) for prod in products]
    products = [{'id': prod.get_id(), 'image': '', 'alt': prod.nome} for prod in products]
    no_admin = Administradores().get_count('') == 0
    is_admin = Administradores().check_access(current_user)
    return render_template('main.html', current_user=current_user, products=products, no_admin=no_admin, is_admin=is_admin)


@app.route('/loja/<_id>')
def loja_id(_id):
    return render_template('shop.html')


@app.route('/cria_loja', methods=['GET'])
def create_shop():
    return render_template('create_shop.html')


@app.route('/loja/<_id>/iventario', methods=['GET'])
def shop_invetory(_id):
    current_user = flask_login.current_user
    shops = ShopAdmins().get_admin_shops(current_user)
    shop = [x for x in shops if x.get_id() == int(_id)][0]
    inventory = Lojas().get_inventory(shop)
    return render_template('shop_invnetory.html', shop=shop, inventory=inventory)


@app.route('/loja/editar', methods=['GET', 'POST'])
def edit_shop_id():
    _id = request.form.get('shop_id')
    current_user = flask_login.current_user
    shops = ShopAdmins().get_admin_shops(current_user)
    shop = [x for x in shops if x.get_id() == int(_id)][0]
    if request.method == 'POST':
        name = request.form.get('shop_name') if request.form.get('shop_name') is not None else ''
        address = request.form.get('address') if request.form.get('address') is not None else ''
        changes = 0
        if shop.nome != name:
            shop.nome = name
            changes += 1
        if shop.address != address:
            shop.address = address
            changes += 1
        if changes > 0:
            Lojas().update_shop(shop)
            Lojas().check_writeble_fields()
    return render_template('shop_edit.html', shop=shop, fields=Lojas().get_writeble_fields())


@app.route('/perfil/editar', methods=['GET', 'POST'])
@login_required
def profile_id_edit():
    current_user = flask_login.current_user
    if request.method == 'POST':
        first_name = request.form.get('firstname') if request.form.get('firstname') is not None else ''
        last_name = request.form.get('lastname') if request.form.get('lastname') is not None else ''
        email = request.form.get('email') if request.form.get('email') is not None else ''
        changes = 0
        if current_user.firstname != first_name:
            current_user.firstname = first_name
            changes += 1
        if current_user.lastname != last_name:
            current_user.lastname = last_name
            changes += 1
        if current_user.email != email:
            current_user.email = email
            changes += 1
        if changes > 0:
            Usuarios().update_user(current_user)
    shops = ShopAdmins().get_admin_shops(admin=current_user)
    return render_template('profile_edit.html', current_user=current_user, shops=shops)


@app.route('/perfil/<_id>')
def profile_id(_id):
    return render_template('profile.html', current_user=flask_login.current_user)


@app.route('/perfil/<_id>/loja/<_shop_id>')
def profile_loja_id(_id, _shop_id):
    return render_template('shop_profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login_screen():
    return render_template('login.html')


@app.route('/registrar', methods=['GET', 'POST'])
def register_screen():
    return render_template('register.html')


if __name__ == '__main__':
    app.run(debug=True)
