from flask import session, flash, url_for
from werkzeug.utils import redirect
from models.user import User

def current_user():
    uid = session.get('user_id', -1)
    u = User.find_by_id(uid)
    return u


def login_required(func):
    def wrapper(*args, **kwargs):
        u = current_user()
        if u is not None:
            return func(*args, **kwargs)
        else:
            flash('你尚未登录')
            return redirect(url_for('index.index'))
    wrapper.__name__ = func.__name__
    return wrapper