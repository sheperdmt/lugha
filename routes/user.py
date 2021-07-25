from flask import (
    render_template,
    Blueprint,
)

from models.memo import Memopad
from models.user import User
from routes.utils import current_user

main = Blueprint('user', __name__)


@main.route('/<username>')
def index(username):
    cu = current_user()
    # TODO 判断是否本人，据此做不同的展示/编辑功能 
    u = User.find_one(username=username)
    memopads = Memopad.find(user_id=u.id)
    return render_template('user.html', username=username, memopads=memopads)