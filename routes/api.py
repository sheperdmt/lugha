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
from models.lexicon import Card, Sema


main = Blueprint('api', __name__)

@main.route('/memo/add', methods=['POST'])
def add():
    data = json.loads(request.data)
    u = current_user()
    u.add_memo(data)
    Sema.batch_add_sema_user(data, u.id)
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
    Sema.batch_delete_sema_user(data, u.id)
    Card.batch_remove_user_card(data, u.id)
    return 'removal success!'