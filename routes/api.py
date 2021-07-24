from models.memo import Memopad
from flask import (
    request,
    Blueprint,
)
import json
from routes import current_user
from models.lexicon import Card, Sema, Word_by_PoS


main = Blueprint('api', __name__)


@main.route('/memo/add', methods=['POST'])
def add():
    u = current_user()
    data = json.loads(request.data)
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
    u = current_user()
    data = json.loads(request.data)
    u.remove_memo(data)
    Sema.batch_delete_sema_user(data, u.id)
    Card.batch_remove_user_card(data, u.id)
    return 'removal success!'

@main.route('/memo/load_saved_ones', methods=['POST'])
def load_saved_ones():
    d = json.loads(request.data)
    u = current_user()
    semas = u.load_saved_ones(d)
    data = json.dumps(semas)
    return data

@main.route('/memo/load_some', methods=['POST'])
def load_some():
    d = json.loads(request.data)
    quantity = d.get('quantity')
    u = current_user()
    semas = u.load_some_semas(quantity)
    data = json.dumps(semas)
    return data

@main.route('/memo/detail')
def load_card():
    sema_id = request.args.get('id')
    sema = Sema.find_by_id(sema_id)
    prfl = sema.profile()
    data = json.dumps(prfl)
    return data

@main.route('/memo/note')
def load_note():
    u = current_user()
    sema_id = request.args.get('id')
    card = Card.find_one(sema_id=int(sema_id), user_id=u.id)
    data = card.note
    return data

@main.route('/memo/note/save', methods=['POST'])
def save_note():
    u = current_user()
    d = json.loads(request.data)
    sema_id = d.get('sema_id')
    card = Card.find_one(sema_id=int(sema_id), user_id=u.id)
    card.note = d.get('note')
    card.save()
    return 'success!'

@main.route('/memo/note/get_memopads')
def get_memopads():
    u = current_user()
    memopads = Memopad.find(user_id=u.id)
    data = []
    for m in memopads:
        data.append(dict(
            id=m.id,
            name=m.name,
            memo_no=m.memo_no,
            desc=m.description,
        ))
    data = json.dumps(data)
    return data

@main.route('/memo/note/get_memopads_of_the_card')
def get_memopads_of_the_card():
    sema_id = request.args.get('id')
    card = Card.find_one(sema_id=int(sema_id))
    memo_ids = card.memos_list
    data = json.dumps(memo_ids)
    return data

@main.route('/memo/note/get_memopad_objects_of_the_card')
def get_memopad_objects_of_the_card():
    sema_id = request.args.get('id')
    card = Card.find_one(sema_id=int(sema_id))
    memopads = card.get_memos_list()
    data = json.dumps(memopads)
    return data

@main.route('/memo/note/add_to_memopad', methods=['POST'])
def add_to_memopad():
    u = current_user()
    sema_id = request.args.get('id')
    memo_id_dict = json.loads(request.data)
    card = Card.find_one(sema_id=int(sema_id), user_id=u.id)
    print('memo_id_dict',memo_id_dict)
    print('card before', card)
    for k, v in memo_id_dict.items():
        memopad = Memopad.find_by_id(id=int(k))
        if v > 0:
            if sema_id not in memopad.content:
                memopad.content.append(sema_id)
            card.add_to_memos_list(int(k))
        else:
            if sema_id in memopad.content:
                memopad.content.remove(sema_id)
            card.delete_from_memos_list(int(k))
        memopad.save()
    print('card after', card)
    card.save()
    return 'success!'

@main.route('/memo/note/new_memopad', methods=['POST'])
def new_memopad():
    data = json.loads(request.data)
    name = data.get('name')
    desc = data.get('desc')
    u = current_user()
    memo_no = Memopad.get_new_memo_no(u.id)
    memopad = Memopad.new(user_id=u.id, name=name, description=desc, memo_no=memo_no)
    memopad.save()
    return 'success!'