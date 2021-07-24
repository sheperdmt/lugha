from models import Model
import hashlib
from models.memo import Memopad
from models.lexicon import Sema, Card

def encrypted(pswd, salt='2hj4twk#^er_=gs-dnvxfxtASD!.]u8a59eyht'):
    s = pswd + salt
    s = s.encode()
    return hashlib.sha256(s).hexdigest()


class User(Model):
    def __init__(self):
        super().__init__()
        self.username = ''
        self.password = ''
        self.role = 10
        self.memo = []

    @classmethod
    def register(cls, form):
        if cls.validate_register(form):
            u = cls.new(form)
            u.password = encrypted(u.password)
            u.save()
            return u

    @classmethod
    def validate_register(cls, form):
        username = form['username']
        password = form['password']
        if not cls.has(username=username):
            if len(username) > 5:
                if username.isascii():
                    return password.isascii()

    @classmethod
    def login(cls, form):
        username = form['username']
        password = form['password']
        u = cls.find_one(username=username)
        if u is not None:
            if u.password == encrypted(password):
                return u

    def _add_memo(self, sema_id_list):
        for i in sema_id_list:
            if i not in self.memo:
                self.memo.append(i)
        self.save()
            
    def remove_memo(self, data):
        for i in data:
            if i in self.memo:
                self.memo.remove(i)
        self.save()

    def load_memo(self):
        return self.memo

    def load_saved_ones(self, sema_id_list):
        data = []
        for s in sema_id_list:
            if s in self.memo:
                data.append(s)
        return data

    def load_some(self, quantity=100):
        return self.memo[:quantity]

    def add_to_default_memo(self, sema_id_list):
        memo = Memopad.find_one(user_id=self.id, memo_no=0)
        if memo is None:
            memo = Memopad.new(user_id=self.id, memo_no=0, name='默认单词本')
        for i in sema_id_list:
            if i not in memo.content:
                memo.content.append(i)
                card = Card.new_card(i, self.id)
                card.add_to_memos_list(memo.id)
        memo.save()

    def add_memo(self, sema_id_list):
        self._add_memo(sema_id_list)
        self.add_to_default_memo(sema_id_list)

    def load_some_semas(self, quantity):
        sema_id_list = self.load_some(quantity)
        semas = (Sema.find_by_id(s) for s in sema_id_list)
        data = []
        for i in semas:
            card = Card.find_one(sema_id=i.id)
            memopads = card.get_memos_list()
            sema_data = dict(id=i.id, lemma=i.lemma, lang=i.lang, pos=i.pos, content=i.content, memopads=memopads)
            data.append(sema_data)
        return data
