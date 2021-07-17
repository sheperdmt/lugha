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

from parser import get_page, word_into_model, initialize_new_headword
from parser import run as word_parser
from parser.get_language_list import get_possible_language_list
from linguistics import code2name, name2code

main = Blueprint('word', __name__)

NO_SUCH_WORD = '查无此词'
WRONG_INPUT = '输入有误'


@main.route("/search")
@login_required
def search():
    word = request.args.get('word')
    if word is None:
        flash('输入有误')
        return redirect(url_for('index.index'))
    
    if Headword.does_word_exist(word):      # 曾被查询过的情况
        if Headword.is_word_valid(word) == False:   # 垃圾输入的情况
            flash(NO_SUCH_WORD)
            return redirect(url_for('index.index'))
        h = Headword.find_one(lemma=word)
        lang = h.first_valid_lang() # 返回第一个有效语言
        word_repr = f'{word}.{lang}'
        return redirect(url_for('.index', word_repr=word_repr))

    else:       # 未被查询过的情况
        possible_language_list = get_possible_language_list(word)   # 这一步会下载网页，找到语言列表
        if len(possible_language_list) > 0:
            lang = initialize_new_headword(word, possible_language_list) # 按顺序，在六种默认语言中找，找到的第一个存入数据库
            if lang is None:    # 没有找到的情况，让用户选择其他语言
                langs_repr = '.'.join(possible_language_list)
                return redirect(url_for('.quo_vadis', word=word, langs=langs_repr))
            else:   # 如果找到了六种之一
                word_repr = f'{word}.{lang}'
                return redirect(url_for('.index', word_repr=word_repr))
        else:   # Wiktionary 上没有这个语言的情况
            flash(NO_SUCH_WORD)
            return redirect(url_for('index.index'))


@main.route("/quo-vadis")
@login_required
def quo_vadis():
    word = request.args.get('word')
    data = Headword.all_possible_langs(word)
    return render_template('word/quo_vadis.html', word=word, data=data)


@main.route('/<word_repr>')
def index(word_repr):
    w, l = word_repr.rsplit('.', 1)
    entries = Word.find(lemma=w, lang=l)
    if entries == []:    # 新词的情况
        return redirect(url_for('.add', word=w, lang=l))
    # 链接到其他语言要用的数据
    all_possible_langs = Headword.all_possible_langs(w)
    other_possible_langs = [lang for lang in all_possible_langs if lang[0] != l]
    # 词条数据
    data = Word.data_for_word_page(w, l)
    return render_template(
        'word/index.html',
        lemma=w,
        lang=code2name(l),
        data=data,
        other_possible_langs=other_possible_langs,
    )


@main.route('/add')
@login_required
def add():
    word = request.args.get('word')
    lang = request.args.get('lang')
    h = Headword.find_one(lemma=word)
    if h is not None:   # 是否存在这个 headword
        if lang in h.possible_langs():
            word_parser(word, lang)
            word_repr = f'{word}.{lang}'
            return redirect(url_for('.index', word_repr=word_repr))
    flash(NO_SUCH_WORD)
    return redirect(url_for('index.index'))