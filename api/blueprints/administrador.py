import flask_login
from flask import Blueprint, render_template, abort, request, redirect, url_for
from flask_login import login_required
from jinja2 import TemplateNotFound

from blueprints.api import api_auth

admin = Blueprint('admin', __name__,
                  template_folder='../templates')


@admin.route('/admin')
@login_required
def adm_home():
    try:
        return render_template('admin/home.html')
    except TemplateNotFound:
        abort(404)


@admin.route('/admin/principal')
@login_required
def adm_main():
    try:
        return render_template('admin/main.html', current_user=flask_login.current_user)
    except TemplateNotFound:
        abort(404)


@admin.route('/admin/login', methods=['GET', 'POST'])
def adm_login():
    try:
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            res = api_auth(username, password)
            if res.get('auth') == 'success':
                return redirect(url_for('adm_home'))
        return render_template(f'admin/login.html')
    except TemplateNotFound:
        abort(404)
