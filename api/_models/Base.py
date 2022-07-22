class Base:
    def from_dict(self, dict_product: dict):
        for key in dict_product:
            if key in self.__dict__.keys():
                setattr(self, key, dict_product[key])
        return self

    def as_list(self):
        return list(self.__dict__.values())

    def keys_as_list(self):
        return list(self.__dict__.keys())
