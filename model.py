
class Model(object):
    def __new__(cls, mongo_doc):
        if mongo_doc is None:
            return None
        return super(Model, cls).__new__(cls)

    def __init__(self, mongo_doc):
        object.__setattr__(self, "_mongo_doc", mongo_doc)

    @property
    def mongo_document(self):
        return self._mongo_doc

    def __getattr__(self, attr):
        if attr in self._mongo_doc:
            return self._mongo_doc[attr]
        return None

    def __getitem__(self, key):
        return self.__getattr__(key)

    def __setattr__(self, attr, value):
        self._mongo_doc[attr] = value

    def __setitem__(self, key, value):
        return self.__setattr__(key, value)
