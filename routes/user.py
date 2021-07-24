from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    flash,
)

from models.lexicon import Card, Sema
from models.memo import Memopad
from models.user import User
from routes.utils import current_user

main = Blueprint('user', __name__)


@main.route('/<username>')
def index(username):
    cu = current_user()
    u = User.find_one(username=username)
    u.memo
    memo = [Sema.find_by_id(m) for m in u.memo]


    memopads = Memopad.find(user_id=u.id)


    return render_template('user.html', username=username, memo=memo, memopads=memopads)