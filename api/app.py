import datetime

import flask_login
from flask import Flask, request, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from flask_login import LoginManager, login_user, login_required
from flask_toastr import Toastr

from _models.Inventory import Inventory
from _models.Product import Product
from _models.Shop import Shop
from _models.ShopAdmin import ShopAdmin
from _models.User import User
from blueprints.administrator import admin
from dao.inventories import Inventories
from dao.products import Products
from dao.shop_admins import ShopAdmins
from dao.shops import Shops
from dao.users import Users

app = Flask(__name__)
app.register_blueprint(admin)
bootstrap = Bootstrap5(app)
toastr = Toastr(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_pyfile("instance/config.py")


@login_manager.user_loader
def load_user(user_id):
    user = Users().get_user_by_id(user_id=user_id)
    if user is None:
        return None
    return user if user_id == user.get_id() else None


@app.route('/')
def root():
    current_user = flask_login.current_user
    shops = Shops().to_list_of_class_object('', Shop)
    products = Inventories().to_list_of_class_object('', Inventory)[:10]
    products = [Products().to_class_object(f"_id = '{prod.product_id}'", Product) for prod in products]
    products = [{'id': prod.get_id(), 'image': '', 'alt': prod.name} for prod in products]
    return render_template('main.html', current_user=current_user, shops=shops, products=products)


@app.route('/shop/<_id>')
def loja_id(_id):
    return render_template('shop.html')


@app.route('/create_shop', methods=['GET'])
def create_shop():
    return render_template('create_shop.html')


@app.route('/shop/<_id>/inventory', methods=['GET'])
def shop_invetory(_id):
    current_user = flask_login.current_user
    shops = ShopAdmins().get_admin_shops(current_user)
    shop = [x for x in shops if x.get_id() == int(_id)][0]
    inventory = Shops().get_inventory(shop)
    return render_template('shop_invnetory.html', shop=shop, inventory=inventory)


@app.route('/shop/<_id>/edit', methods=['GET', 'POST'])
def edit_shop_id(_id):
    current_user = flask_login.current_user
    shops = ShopAdmins().get_admin_shops(current_user)
    shop = [x for x in shops if x.get_id() == int(_id)][0]
    if request.method == 'POST':
        name = request.form.get('shop_name') if request.form.get('shop_name') is not None else ''
        address = request.form.get('address') if request.form.get('address') is not None else ''
        changes = 0
        if shop.name != name:
            shop.name = name
            changes += 1
        if shop.address != address:
            shop.address = address
            changes += 1
        if changes > 0:
            Shops().update_shop(shop)
            Shops().check_writeble_fields()
    return render_template('shop_edit.html', shop=shop, fields=Shops().get_writeble_fields())


@app.route('/shop/<_id>/product/<_product_id>')
def shop_product_id(_id, _product_id):
    return render_template('product.html')


@app.route('/shop/<_id>/product/<_product_id>/edit', methods=['GET', 'POST'])
def edit_shop_product(_id, _product_id):
    shop = Shops().get_shop_by_id(_id)
    product = Products().to_class_object(f'_id = {_product_id}', Product) if _product_id != 'new' else Product()
    if product is None:
        return redirect(shop_invetory(_id))
    if request.method == 'POST':
        if request.form.get('save'):
            if _product_id == 'new':
                product = Product().from_dict(request.form)
                product_id = Products().get_count('') + 1 if product.get_id() == '' else product.get_id()
                product._id = product_id
                res = Products().register(product)
                if res.get('error') is None:
                    res2 = Inventories().register(Inventory(product_id=product_id, shop_id=_id, quantity=0))
            else:
                product = Product().from_dict(request.form)
                res = Products().update(where=f"_id = '{_product_id}'",
                                        updated_object=product,
                                        class_reference=Product)
                if res.get('error') is None:
                    res2 = Inventories().update(where=f"product_id = '{_product_id}'",
                                                updated_object=Inventory(product_id=product.get_id(), shop_id=_id,
                                                                         quantity=0),
                                                class_reference=Inventory)
            if res.get('error'):
                flash(res.get('error'), 'error')
            else:
                flash(res.get('success'), 'success')
                return redirect(f"/shop/{_id}/product/{product.get_id()}/edit")
        elif request.form.get('delete'):
            res = Products().delete(f"_id = '{_product_id}'")
            if res.get('error') is None:
                res = Inventories().delete(f"product_id = '{_product_id}' AND shop_id = '{_id}'")
                if res.get('error') is None:
                    flash(res, 'success')
                else:
                    flash(res, 'error')
            else:
                flash(res, 'error')
            return redirect(f'/shop/{_id}/inventory')
    return render_template('product_edit.html', product=product, shop=shop)


@app.route('/profile/<_id>/edit', methods=['GET', 'POST'])
@login_required
def profile_id_edit(_id):
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
            Users().update_user(current_user)
    shops = ShopAdmins().get_admin_shops(admin=current_user)
    return render_template('profile_edit.html', current_user=Users().get_user_by_username(username=_id), shops=shops)


@app.route('/profile/<_id>')
def profile_id(_id):
    return render_template('profile.html', current_user=flask_login.current_user)


@app.route('/profile/<_id>/shop/<_shop_id>')
def profile_loja_id(_id, _shop_id):
    return render_template('shop_profile.html')


@app.route('/login', methods=['GET', 'POST'])
def login_screen():
    if request.method == 'POST':
        username = request.form.get('lg_username')
        password = request.form.get('lg_password')
        res = Users().login(username, password)
        if res.json['error'] is None:
            login_user(res)
            flash("Usuario cadastrado", "success")
            redirect('/')
        else:
            flash(res.json['error'], 'error')
    return render_template('home.html')


@app.route('/api/login', methods=['GET', 'POST'])
def api_login():
    username = ''
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        res = Users().login(username=username, password=password)
        user = res.get('user')
        if user is not None:
            try:
                ress = login_user(user, duration=datetime.timedelta(days=7), remember=True)
                print(ress)
            except Exception as e:
                print(e)
            # session['_id'] = res.get('token')
            # request.cookies['remember_token'] = res.get('token')
            flash('Login com sucesso', 'success')
        else:
            flash(res.get('error'), 'error')
    return redirect(url_for('root'))


@app.route('/api/register_shop', methods=['POST'])
def api_register_shop():
    if request.method == 'POST':
        shop_name = request.form.get('name')
        shop_adress = request.form.get('address')
        shop_id = Shops().get_count('') + 1
        res = Shops().register(Shop(_id=shop_id, name=shop_name, address=shop_adress))
        res_adm = ShopAdmins().register(ShopAdmin().from_dict(
            {'user_id': flask_login.current_user.get_id(), 'shop_id': shop_id, 'status': 'active'}))
        if res.get('error') is not None or res_adm.get('error') is not None:
            flash(str(res.get('error')), 'error')
        else:
            flash(res.get('message'), 'success')
    return redirect(url_for('profile_id_edit', _id=flask_login.current_user.username))


@app.route('/api/register_product', methods=['POST'])
def api_register_product():
    if request.method == 'POST':
        product_name = request.form.get('name')
        unity_type = request.form.get('unity_type')
        selling_price = request.form.get('selling_price')
        cost_price = request.form.get('cost_price')
        barcode = request.form.get('barcode')
        bought_from = request.form.get('bought_from')
        product_id = Products().get_count('') + 1
        product = Product(_id=product_id, name=product_name, unity_type=unity_type, selling_price=selling_price,
                          cost_price=cost_price, barcode=barcode, bought_from=bought_from)
        res = Products().register(product)
        if res.get('error') is not None:
            flash(str(res.get('error')), 'error')
        else:
            flash(res.get('message'), 'success')
    return redirect(url_for('edit_shop_product', _id=flask_login.current_user.username))


@app.route('/api/register', methods=['GET', 'POST'])
def api_register():
    username = request.form.get('username')
    password = request.form.get('password')
    first_name = request.form.get('firstname')
    last_name = request.form.get('lastname')
    email = request.form.get('email')
    repassword = request.form.get('repassword')
    if username is None or password is None or first_name is None or last_name is None or email is None or repassword is None:
        flash("missing info", 'error')
    elif password != repassword:
        flash("Password not matching", 'error')
    else:
        _id = Users().get_count(where='') + 1
        res = Users().register(
            User(_id=_id, username=username, password=password, email=email, firstname=first_name, lastname=last_name))
        if res.get('error'):
            flash(str(res.get('error')), 'error')
            return redirect('/login')
        elif res.get('token'):
            flash('Registrado com sucesso', 'success')
    return redirect('/')


@app.route('/api/logout', methods=['GET', 'POST'])
def api_logout():
    flask_login.logout_user()
    flash('Logged out', 'Success')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
