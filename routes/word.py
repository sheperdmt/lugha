from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    flash,
)

from .utils import (
    login_required,
    current_user,
)

from models.lexicon import (
    Headword,
    Word,
    Word_by_PoS,
    Sema,
)

from parser import get_page, word_into_model, new_headword_run
from parser import run as word_parser
from parser.get_language_list import get_possible_language_list
from linguistics import PARTS_OF_SPEECH, PARTS_OF_SPEECH_ABBR, to_canonical_names, code_lang_normalizer

main = Blueprint('word', __name__)

pos_dict = dict(zip(PARTS_OF_SPEECH_ABBR, PARTS_OF_SPEECH))

@main.route("/search")
@login_required
def search():
    word = request.args.get('word')
    if word is None:
        return redirect(url_for('index.index'))
    if Headword.does_word_exist(word):
        if Headword.is_word_valid(word) == False:
            no_such_word = '查无此词'
            flash(no_such_word)
            return redirect(url_for('index.index'))
        h = Headword.find_one(lemma=word)
        lang = h.first_valid_lang()
        word_repr = f'{word}.{lang}'
        return redirect(url_for('word.index', word=word_repr))
    else:
        possible_language_list = get_possible_language_list(word)
        if len(possible_language_list) > 0:
            lang = new_headword_run(word, possible_language_list)
            if lang is None:
                return render_template('word/quo_vadis.html', word=word, 
                    languages=possible_language_list, to_canonical_names=to_canonical_names,
                    code_lang_normalizer=code_lang_normalizer)
            else:
                lang = code_lang_normalizer(lang)
                word_repr = f'{word}.{lang}'
                return redirect(url_for('.index', word=word_repr))
        else:
            no_such_word = '查无此词'
            flash(no_such_word)
            return redirect(url_for('index.index'))


@main.route('/<word>')
def index(word):
    w, l = word.rsplit('.', 1)
    entries = Word.find(lemma=w, lang=l)
    u = current_user()
    if entries == []:
        if u is not None:
            h = Headword.find_one(lemma=w)
            if h is not None:
                if l in h.possible_langs():
                    return redirect(url_for('.add', word=word))
        no_such_word = '查无此词'
        flash(no_such_word)
        return redirect(url_for('index.index'))
    h = Headword.find_one(lemma=w)
    languages = h.possible_langs()
    return render_template(
        'word/index.html',
        word=w,
        lang=l,
        entries=entries,
        languages=languages,
        to_canonical_names=to_canonical_names,
        code_lang_normalizer=code_lang_normalizer,
        pos_dict=pos_dict,
        Word_by_PoS=Word_by_PoS,
        Sema=Sema,
    )

@main.route('/add/<word>')
@login_required
def add(word):
    w, l = word.rsplit('.', 1)
    word_parser(w, to_canonical_names(l))
    return redirect(url_for('.index', word=word))