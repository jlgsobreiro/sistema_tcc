import datetime
import json

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

contas = Blueprint('contas', __name__)


@contas.route('/contas', methods=['POST', 'GET'])
def main():
    return render_template('admin/contas/main.html', fornecedores=json.dumps(['teste', 'teste1']))
