class BaseModel:

    def get_all(self):
        raise Exception('Implementar função')

    def instance_reference(self):
        raise Exception('Implementar função')

    def to_dict(self):
        to_dict = {}
        for value in self:
            if value != 'id':
                to_dict[value] = getattr(self, value)
        return to_dict

    def get_all_to_dict_list(self):
        return [x.to_dict() for x in self.get_all()]

    def save_object_from_dict(self, sql_dict):
            self.from_dict_to_self(sql_dict)
            self.save()

    def from_dict_to_self(self, sql_dict: dict):
        for key in sql_dict.keys():
            setattr(self, key, sql_dict[key])
        return self
