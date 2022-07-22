from flask import Blueprint, render_template, abort
from jinja2 import TemplateNotFound

admin = Blueprint('admin', __name__,
                  template_folder='../templates')


@admin.route('/', defaults={'page': 'index'})
@admin.route('/<page>')
def show(page):
    try:
        return render_template(f'admin/login.html')
    except TemplateNotFound:
        abort(404)
