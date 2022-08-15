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

estoque = Blueprint('estoque', __name__)


@estoque.route('/estoque')
def main():
    return render_template('admin/estoque/main.html')
