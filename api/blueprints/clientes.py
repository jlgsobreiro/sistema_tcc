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
from dao.shop_admins import ShopAdmins
from dao.lojas import Lojas
from dao.usuarios import Usuarios

clientes = Blueprint('clientes', __name__)


@clientes.route('/clientes')
def main():
    _clientes = Usuarios().to_list_of_class_object(where='', class_reference=Usuario)
    return render_template('admin/clientes/main.html', clientes=_clientes)
