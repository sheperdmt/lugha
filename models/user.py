from models import Model
import hashlib


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

    def add_memo(self, data):
        for i in data:
            if i not in self.memo:
                self.memo.append(i)
                self.save()
            