class BaseMongo:
    meta = {"allow_inheritance": True}

    @classmethod
    def get(cls, id=None, **kwargs):
        if id:
            kwargs['id'] = id
        return cls.Meta.model.objects(**kwargs)

    @classmethod
    def find(cls, **kw):
        return cls.Meta.model.objects(**kw)

    @classmethod
    def find_one(cls, **kw):
        return cls.Meta.model.objects(**kw).first()

    @classmethod
    def create(cls, **kwargs):
        instance = cls.Meta.model()
        for k, v in kwargs.items():
            setattr(instance, k, v)

        instance.save()
        return instance
    @classmethod
    def get_all_as_dict_list(cls):
        return [x.to_mongo() for x in cls.Meta.model.objects()]

    @classmethod
    def all(cls, limit=None):
        return cls.fetch_by().limit(limit)

    @classmethod
    def get_all_to_dict_list(cls):
        return [x.to_dict() for x in cls.Meta.model.objects()]

    @classmethod
    def to_dict(cls):
        to_dict = {}
        for value in cls.Meta.model:
            if value != 'id':
                to_dict[value] = getattr(cls.Meta.model, value)
        return to_dict

    # NOME_TABELA = ''
    # BANCO_DE_DADOS = "api/database.db"
    #
    # meta = {'allow_inheritance': True, 'db_alias': NOME_TABELA}
    #
    # def registrar(self, obj: object):
    #     obj.__dict__.pop('_id')
    #     return self.insere_na_tabela(obj.__dict__)
    #
    # def insere_na_tabela(self, item: dict):
    #     mongo_conn = self.database_get_connection()
    #     try:
    #         return mongo_conn.insert_one(item).inserted_id
    #     except Exception as e:
    #         return {'error': e}
    #
    # def apagar_por_id(self, obj_id):
    #     mongo_conn = self.database_get_connection()
    #     try:
    #         return mongo_conn.find_one_and_delete({'_id': ObjectId(obj_id)})
    #     except Exception as e:
    #         return {'error': e}
    #
    # def para_objeto(self, obj_id: str, class_reference: object):
    #     mongo_conn = self.database_get_connection()
    #     mongo_obj = mongo_conn.find_one({'_id': ObjectId(obj_id)})
    #     return class_reference().from_dict(mongo_obj) if mongo_obj is not None else mongo_obj
    #
    # def para_dict(self, obj_id: str):
    #     mongo_conn = self.database_get_connection()
    #     obj_id = ObjectId(obj_id)
    #     mongo_obj = mongo_conn.find_one({'_id': obj_id})
    #     return json.loads(json_util.dumps(mongo_obj))
    #
    # def para_lista_de_objetos(self, filtro: dict, class_reference: object):
    #     mongo_conn = self.database_get_connection()
    #     mongo_objs = mongo_conn.find(filtro)
    #     list_objs = []
    #     for obj in mongo_objs:
    #         list_objs.append(class_reference().from_dict(obj))
    #     return list_objs
    #
    # def para_lista_de_dict(self, filtro: dict):
    #     mongo_conn = self.database_get_connection()
    #     mongo_objs = mongo_conn.find(filtro)
    #     list_objs = []
    #     for obj in mongo_objs:
    #         list_objs.append(json.loads(json_util.dumps(obj)))
    #     return list_objs
    #
    # def atualizar(self, objeto_atualizado, class_reference: object):
    #     object_to_update = self.para_objeto(objeto_atualizado.id, class_reference=class_reference)
    #     if objeto_atualizado == object_to_update:
    #         return None
    #     values = {}
    #     for key in object_to_update.__dict__:
    #         if objeto_atualizado.__dict__[key] != object_to_update.__dict__[key]:
    #             if objeto_atualizado.__dict__[key] is not None or object_to_update.__dict__[key] is not None:
    #                 values[key] = objeto_atualizado.__dict__[key]
    #     mongo_conn = self.database_get_connection()
    #     try:
    #         return mongo_conn.find_one_and_update({'_id': objeto_atualizado._id}, {'$set': values})
    #     except Exception as e:
    #         return {'error': e}
    #
    # def conta_itens(self, filtro: dict):
    #     mongo_conn = self.database_get_connection()
    #     return mongo_conn.count_documents(filtro)
