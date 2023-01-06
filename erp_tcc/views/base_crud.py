import ft as ft
from flask import render_template, request, flash, redirect, url_for
from flask.views import View, MethodView
from flask_mongoengine.wtf import model_form
from flask_wtf import FlaskForm
from mongoengine import Document
import wtforms.fields as wtf_fields
from wtforms.validators import DataRequired

from repository.base_mongo import BaseMongo


class MetaForm(FlaskForm):
    def __init__(self, model: Document, *args, **kwargs):
        super().__init__(*args, **kwargs)
        fields = [(x, model._fields[x]) for x in model._fields if x != 'id']
        for field_name, field_type in fields:
            wtforms_field = getattr(wtf_fields, str(field_type.__class__.__name__))
            field_instance = wtforms_field(label=field_name, validators=[DataRequired()], value='')
            print(field_instance.__dict__)
            setattr(self, field_name, field_instance)
        self.populate_obj(model)



class SimpleCRUD:
    permissoes = ['create', 'edit', 'delete']
    links_nav_bar = []
    title = ''
    form = None
    table = None

    # def dispatch_request(self):
    #     delete_url = f'delete_view'
    #     edit_url = f'edit_view'
    #     _id = request.form.get('id', '')
    #     print(_id)
    #     print(delete_url)
    #     print(edit_url)
    #     print(self.links_nav_bar)
    #     self.table = self.Meta.meta().get_all_to_dict_list()
    #     print(self.table)
    #     try:
    #         return render_template('crud.html',
    #                                title=self.title,
    #                                links_nav_bar=self.links_nav_bar,
    #                                form=self.form,
    #                                table=self.table,
    #                                permissions=self.permissoes,
    #                                delete_url=delete_url,
    #                                edit_url=edit_url,
    #                                id=_id)
    #     except Exception as e:
    #         print('Erro: ', e)
    #         return render_template('not_found.html')

    def head(self):
        print('teste head')
        delete_url = f'delete_view'
        edit_url = f'edit_view'
        _id = request.form.get('id', '')
        print(_id)
        print(delete_url)
        print(edit_url)
        print(self.links_nav_bar)
        self.table = self.Meta.meta().get_all_to_dict_list()
        print(self.table)
        return render_template('crud.html',
                               title=self.title,
                               links_nav_bar=self.links_nav_bar,
                               form=self.form,
                               table=self.table,
                               permissions=self.permissoes,
                               delete_url=delete_url,
                               edit_url=edit_url,
                               id=_id)

    def get(self):
        print('teste get')
        delete_url = f'delete'
        edit_url = f'edit_view'
        _id = request.form.get('id', '')
        print(_id)
        print(delete_url)
        print(edit_url)
        print(self.links_nav_bar)
        self.table = self.Meta.meta().get_all_to_dict_list()
        print(self.table)
        try:
            return render_template('crud.html',
                                   title=self.title,
                                   links_nav_bar=self.links_nav_bar,
                                   form=self.form,
                                   table=self.table,
                                   permissions=self.permissoes,
                                   delete_url=delete_url,
                                   edit_url=edit_url,
                                   id=_id)
        except Exception as e:
            print('Erro: ', e)
            return render_template('not_found.html')

    def post(self):
        pass

    def put(self):
        pass

    def delete(self, id_item):
        pass

    @classmethod
    def get_repository(cls):
        base_repository = BaseMongo
        base_repository.meta = cls.Meta.meta
        return base_repository

    @classmethod
    def table_view(cls):
        _id = request.form.get('id', '')

        cls.table = cls.Meta.repo().get_all_to_dict_list()
        print(cls.table)
        try:
            print('opa')
            return render_template('crud.html',
                                   title=cls.title,
                                   links_nav_bar=cls.links_nav_bar,
                                   form=cls.form,
                                   table=cls.table,
                                   permissions=cls.permissoes,
                                   cls_endpoint=cls.__name__.lower(),
                                   id=_id)
        except Exception as e:
            print('Erro: ', e)
            return render_template('not_found.html')

    @classmethod
    def edit_view(cls, id_item=None):
        edit_data = cls.Meta.repo().find_one(id=id_item)
        edit_form = model_form(edit_data)
        form = edit_form(request.form)
        print(id_item)
        if request.method == "PUT":
            edit_form.populate_obj(edit_data)
            edit_data.save()
        return render_template("edit.html", title=cls.title, links_nav_bar=cls.links_nav_bar, form=form)

    @classmethod
    def delete_view(cls, id_item=None):
        flash('apagando')
        cls.Meta.repo().find_one(id=id_item).delete()
        print(id_item)
        return cls.table_view()

    def delete(self, id_item=None):
        print(id_item)

    @classmethod
    def create_view(cls):
        form = MetaForm(cls.Meta.meta())
        # form = model_form(cls.Meta.meta())

        return render_template("crud.html", title=cls.title, links_nav_bar=cls.links_nav_bar, form=form)

    @classmethod
    def url_rule_table(cls):
        return f'/{cls.__name__.lower()}', cls.table_view

    @classmethod
    def url_rule_edit(cls):
        return f'/{cls.__name__.lower()}/edit/<id_item>', cls.edit_view

    @classmethod
    def url_rule_delete(cls):
        return f'/{cls.__name__.lower()}/delete/<id_item>', cls.delete_view

    @classmethod
    def url_rule_create(cls):
        return f'/{cls.__name__.lower()}/create', cls.create_view
