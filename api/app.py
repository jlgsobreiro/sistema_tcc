import datetime
import http
from asyncio import sleep

import flask
import flask_login
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap5
from flask import Flask, request, render_template, flash, redirect, session, Response, url_for
from flask_toastr import Toastr
from flask_login import LoginManager, login_user, login_required
from requests import post

from _models.User import User
from dao.users import Users

app = Flask(__name__)
bootstrap = Bootstrap5(app)
toastr = Toastr(app)
login_manager = LoginManager()
login_manager.init_app(app)

app.config.from_pyfile("instance/config.py")


@login_manager.user_loader
def load_user(user_id):
    user = Users().get_user_by_username(username=user_id)
    if user is None:
        return None
    return user if user_id == user.username else None


@app.route('/')
def root():
    current_user = flask_login.current_user
    return render_template('main.html', current_user=current_user)


@app.route('/shop/<_id>')
def loja_id(_id):
    return render_template('shop.html')


@app.route('/shop/<_id>/edit')
def edit_loja_id(_id):
    return render_template('shop_edit.html')


@app.route('/shop/<_id>/product/<_product_id>')
def loja_product_id(_id, _product_id):
    return render_template('product.html')


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
            Users().update_user(user=current_user)
    return render_template('profile_edit.html', current_user=Users().get_user_by_username(username=_id))


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
        res = Users().register(
            User(username=username, password=password, email=email, firstname=first_name, lastname=last_name))
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
