from models.lexicon import Card, Sema
from flask import (
    render_template,
    Blueprint,
)
from models.memo import Memopad
from models.user import User
from routes.utils import current_user

main = Blueprint('memopad', __name__)


@main.route('/<memo_id>')
def index(memo_id):
    memopad = Memopad.find_by_id(memo_id)
    title = memopad.name
    desc = memopad.description
    user_id = memopad.user_id
    u = User.find_by_id(user_id)
    cardlist = []
    for c in memopad.content:
        sema = Sema.find_by_id(c)
        profile = sema.profile()
        card = Card.find_one(sema_id=int(c), user_id=u.id)
        # data = dict(
        #     lemma=sema.lemma,
        #     lang=sema.lang,
        #     pos=sema.pos,
        #     repr=sema.repr,
        #     prnn=profile['prnn'],
        #     etym=profile['etym'],
        #     text=profile['text'],
        #     # note=profile['note'],
        #     examples=sema.examples,
        #     content=sema.content,
        #     note=card.note,
        #     easiness=card.easiness,
        #     interval=card.interval,
        #     repetitions=card.repetitions,
        #     review_time=card.review_time,
        #     )
        # cardlist.append(data)
    return render_template('memopad.html', u=u, memo_id=memo_id, title=title, desc=desc)