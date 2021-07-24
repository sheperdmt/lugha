import time
from pymongo import MongoClient
client = MongoClient()


def next_id(name):
    filter = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }
    kwargs = {
        'filter': filter,
        'update': update,
        'upsert': True,
        'new': True,
    }
    doc = client.db['data_id']
    new_id = doc.find_one_and_update(**kwargs).get('seq')
    return new_id


class Model(object):
    def __init__(self):
        self.id = -1
        self.type = ''
        self.deleted = False
        self.ct = 0
        self.ut = 0

    def __repr__(self):
        class_name = self.__class__.__name__
        properties = (f'{k} = {v}' for k, v in self.__dict__.items())
        nl = '\n'
        return f'<{class_name}: {nl}  {f"{nl}".join(properties)}\n>'

    @classmethod
    def has(cls, **kwargs):
        r = False
        if len(cls.find(**kwargs)) > 0:
            r = True
        return r

    @classmethod
    def new(cls, form=None, **kwargs):
        m = cls._new(form, **kwargs)
        m.id = next_id(cls.__name__)
        return m

    @classmethod
    # 同时供 new 和 _new_with_bson 使用
    def _new(cls, form=None, **kwargs):
        m = cls()
        fields = m.__dict__.copy()
        if form is None:
            form = {}

        for k, v in form.items():
            if k in fields:
                t = type(fields[k])
                setattr(m, k, t(v))

        for k, v in kwargs.items():
            if k in fields:
                t = type(fields[k])
                setattr(m, k, t(v))

        ts = int(time.time())
        m.ct = ts
        m.ut = ts
        m.type = cls.__name__.lower()
        return m

    def save(self):
        name = self.__class__.__name__
        client.db[name].save(self.__dict__)

    @classmethod
    # 供 find 使用
    def _new_with_bson(cls, bson):
        m = cls._new(bson)
        setattr(m, '_id', bson['_id'])
        return m

    @classmethod
    def find(cls, **kwargs):
        name = cls.__name__
        kwargs.update({
            'deleted': False,
        })
        ds = client.db[name].find(kwargs)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def find_one(cls, **kwargs):
        r = cls.find(**kwargs)
        if len(r) > 0:
            return cls.find(**kwargs)[0]
        else:
            return None

    @classmethod
    def find_or_new(cls, **kwargs):
        entry = cls.find_one(**kwargs)
        if entry is None:
            entry = cls.new(**kwargs)
        return entry

    def delete(self):
        name = self.__class__.__name__
        query = {
            'id': self.id,
        }
        values = {
            'deleted': True
        }
        client.db[name].update_one(query, values)

    @classmethod
    def find_by_id(cls, id):
        return cls.find_one(id=int(id))
