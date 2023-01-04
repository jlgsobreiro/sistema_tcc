import ft as ft
from flask import render_template, request, flash, redirect, url_for
from flask.views import View, MethodView
from flask_mongoengine.wtf import model_form

from repository.base_mongo import BaseMongo


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
        base_repository.meta = cls.meta
        return base_repository

    @classmethod
    def table_view(cls):
        table_data = cls.get_repository().find()
        return render_template("table.html", title=cls.title, links_nav_bar=cls.links_nav_bar, data=table_data,
                               permissions=cls.permissoes)

    @classmethod
    def edit_view(cls, id_item):
        edit_data = cls.get_repository().find_one(id=id_item)
        edit_form = model_form(instance=cls.meta)
        form = edit_form(request.form)
        print(id_item)
        if request.method == "PUT":
            edit_form.populate_obj(edit_data)
            edit_data.save()
        return render_template("edit.html", title=cls.title, links_nav_bar=cls.links_nav_bar, form=form)

    @classmethod
    def delete_view(cls, id_item):
        flash('apagando')
        cls.get_repository().find_one(id=id_item).delete()
        print(id_item)
        return cls.table_view()

    def delete(self, id_item):
        print(id_item)

    @classmethod
    def create_view(cls):
        return render_template("crud.html", title=cls.title, links_nav_bar=cls.links_nav_bar)

    @classmethod
    def url_rule_table(cls):
        return f'/{cls.__name__.lower()}/table_view', cls.as_view(f'{cls.__name__.lower()}.table_view')

    @classmethod
    def url_rule_edit(cls):
        return f'/{cls.__name__.lower()}/edit_view/<id_item>', cls.as_view(f'{cls.__name__.lower()}.edit_view')

    @classmethod
    def url_rule_delete(cls):
        return f'/{cls.__name__.lower()}/delete_view/<id_item>', cls.as_view(f'{cls.__name__.lower()}.delete')

    @classmethod
    def url_rule_create(cls):
        return f'/{cls.__name__.lower()}/create_view', cls.as_view(f'{cls.__name__.lower()}.create_view')
