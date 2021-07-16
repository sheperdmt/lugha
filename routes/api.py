from flask import (
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    flash,
)
import json
from routes import current_user


main = Blueprint('api', __name__)

@main.route('/memo/add', methods=['POST'])
def add():
    data = json.loads(request.data)
    u = current_user()
    u.add_memo(data)
    return 'adding success!'

@main.route('/memo/load')
def load():
    u = current_user()
    memos = u.load_memo()
    data = json.dumps(memos)
    return data

@main.route('/memo/remov', methods=['POST'])
def remove():
    data = json.loads(request.data)
    u = current_user()
    u.remove_memo(data)
    return 'removal success!'