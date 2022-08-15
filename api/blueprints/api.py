import datetime

import flask_login
from flask import Blueprint, request, flash, redirect, url_for, json
from flask_login import login_user

from _models.Administrador import Administrador
from _models.Produto import Produto
from _models.Lojas import Lojas
from _models.ShopAdmin import ShopAdmin
from _models.Usuario import Usuario
from dao.administradores import Administradores
from dao.fornecedores import FornecedoresDAO
from dao.produtos import Products
from dao.shop_admins import ShopAdmins
from dao.lojas import Lojas
from dao.usuarios import Usuarios
import uuid

api = Blueprint('api', __name__)


def api_auth(username, password):
    res = Usuarios().login(username=username, password=password)
    user = res.get('user')
    if user is not None:
        try:
            ress = login_user(user, duration=datetime.timedelta(days=7), remember=True)
            print(ress)
        except Exception as e:
            print(e)
        flash('Login com sucesso', 'success')
    else:
        flash(res.get('error'), 'error')
        return {'auth': 'error'}
    return {'auth': 'success'}


@api.route('/api/login', methods=['POST'])
def api_login():
    username = ''
    print(request.referrer)
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        res = api_auth(username, password)
        if res.get('auth') == 'success':
            return redirect(url_for('root'))


@api.route('/api/adm_login', methods=['POST'])
def api_adm_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        res = api_auth(username, password)
        if res.get('auth') == 'success':
            return redirect(url_for('admin.adm_home'))


@api.route('/api/registra_loja', methods=['POST', 'GET'])
def api_register_shop():
    if request.method == 'POST':
        shop_name = request.form.get('name')
        shop_adress = request.form.get('address')
        shop_id = Lojas().get_count('') + 1
        res = Lojas().register(Lojas(_id=shop_id, name=shop_name, address=shop_adress))
        res_adm = ShopAdmins().register(ShopAdmin().from_dict(
            {'user_id': flask_login.current_user.get_id(), 'shop_id': shop_id, 'status': 'active'}))
        if res.get('error') is not None or res_adm.get('error') is not None:
            flash(str(res.get('error')), 'error')
        else:
            flash(res.get('message'), 'success')
    return redirect(url_for('profile_id_edit', _id=flask_login.current_user.username))


@api.route('/api/registra_conta', methods=['POST'])
def api_registra_conta():
    return


@api.route('/api/fornecedores_lista', methods=['POST'])
def api_fornecedores_lista():
    lista_fornecedores = FornecedoresDAO().lista_fornecedores()
    lista_fornecedores += ['teste','teste1']
    res = json.dumps({"res": lista_fornecedores})
    return res


@api.route('/api/registra_produto', methods=['POST'])
def api_register_product():
    if request.method == 'POST':
        product_name = request.form.get('name')
        unity_type = request.form.get('unity_type')
        selling_price = request.form.get('selling_price')
        cost_price = request.form.get('cost_price')
        barcode = request.form.get('barcode')
        bought_from = request.form.get('bought_from')
        product_id = Products().get_count('') + 1
        product = Produto(_id=product_id, name=product_name, unity_type=unity_type, selling_price=selling_price,
                          cost_price=cost_price, barcode=barcode, bought_from=bought_from)
        res = Products().register(product)
        if res.get('error') is not None:
            flash(str(res.get('error')), 'error')
        else:
            flash(res.get('message'), 'success')
    return redirect(url_for('edit_shop_product', _id=flask_login.current_user.username))


@api.route('/api/registrar', methods=['GET', 'POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    email = request.form.get('email')
    repassword = request.form.get('repassword')
    if username is None or password is None or first_name is None or last_name is None or email is None or repassword is None:
        flash("Dados não informados", 'error')
    elif password != repassword:
        flash("Senhas não conferem", 'error')
    else:
        usuario = Usuario(_id=str(uuid.uuid4()), usuario=username, senha=password, email=email, nome=first_name, sobrenome=last_name)
        res = Usuarios().register(usuario)
        if res.get('error'):
            flash(str(res.get('error')), 'error')
            # return redirect('/register')
        elif res.get('message') == 'Success':
            flash('Registrado com sucesso', 'success')
            if Administradores().get_count('') == 0:
                Administradores().register(Administrador(usuario_id=usuario.get_id(), acesso='total', condicao='ativo'))
            return redirect(url_for('root'))
        return redirect(url_for('register_screen'))


@api.route('/api/logout', methods=['GET', 'POST'])
def api_logout():
    flask_login.logout_user()
    flash('Logged out', 'Success')
    return redirect('/')
