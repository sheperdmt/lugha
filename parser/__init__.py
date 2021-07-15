from .parser_with_cache import WiktionaryParser
from models.lexicon import Headword, Word, Word_by_PoS, Sema
from linguistics import *
import json

parser = WiktionaryParser()


def get_page(word, language):
    language = to_canonical_names(language)
    data = parser.fetch(word, language=language, proxies={
        'http': 'socks5://192.168.31.247:9909',
        'https': 'socks5://192.168.31.247:9909',
    })
    return data


pos_dict = dict(zip(PARTS_OF_SPEECH, PARTS_OF_SPEECH_ABBR))
rel_dict = dict(zip(RELATIONS, RELATIONS_ABBR))

the_six_lang_codes = ['en', 'fr', 'de', 'it', 'es', 'la']
# the_six_langs = ['English', 'French', 'German', 'Italian', 'Spanish', 'Latin']


def word_constructor(lemma, lang, etym_id, w):
    word_repr = '<{}>.{}.{}'
    repr = word_repr.format(lemma, lang, etym_id)
    form = dict(
        lemma=lemma,
        lang=lang,
        etym_id=etym_id,
        repr=repr,
        etym=w['etymology'],
        prnn='\n'.join(w['pronunciations']['text']),
    )
    word = Word.new(form)
    word.save()
    word.add_to_counter()
    return word


def word_by_pos_constructor(word, wbp):
    word_by_pos_repr = '<{}>.{}.{}.{}'
    pos = pos_dict[wbp['partOfSpeech']]
    repr = word_by_pos_repr.format(
        word.lemma, word.lang, word.etym_id, pos
    )
    rel = {}
    for r in wbp['relatedWords']:
        rel_type = rel_dict[r['relationshipType']]
        rel[rel_type] = r['words']
    form = dict(
        lemma=word.lemma,
        lang=word.lang,
        etym_id=word.etym_id,
        pos=pos,
        repr=repr,
        text=wbp['text'][0],
        rel=rel,
    )
    word_by_pos = Word_by_PoS.new(form)
    word_by_pos.save()
    return word_by_pos


def word_into_model(word_name, language, word_data):
    sema_repr = '<{}>.{}.{}.{}.{}'
    lang = code_lang_normalizer(language)
    count = 0
    for w in word_data:
        count += 1
        word = word_constructor(word_name, lang, count, w)
        for wbp in w['definitions']:
            word_by_pos = word_by_pos_constructor(word, wbp)
            for i in wbp['text'][1]:
                repr = sema_repr.format(
                    word.lemma, word.lang, word.etym_id, word_by_pos.pos, i
                )
                content = wbp['text'][1][int(i)]
                examples = wbp['examples'][int(i)]
                form = dict(
                    lemma=word.lemma,
                    lang=word.lang,
                    etym_id=word.etym_id,
                    pos=word_by_pos.pos,
                    sema_id=int(i),
                    repr=repr,
                    content=content,
                    examples=examples,
                )
                sema = Sema.new(form)
                sema.save()


def run(word_name, language):
    print('*** paring word', word_name, language)
    data = get_page(word_name, language)
    word_into_model(word_name, language, data)


def new_headword_run(word, possible_language_list):    
    for lang in possible_language_list:
        if lang in the_six_lang_codes:
            data = get_page(word, to_canonical_names(lang))
            word_into_model(word, code_lang_normalizer(lang), data)
        else:
            headword = Headword.find_or_new(lemma=word)
            headword.add_possible_lang(lang)


def test(word_name, language):
    data = get_page(word_name, language)
    print('data, ', data)
    print('type of data, ', type(data))
    word_into_model(word_name, language, data)
    with open(f'./temp/{word_name}-{language}.txt', 'w', encoding='utf-8') as f:
        d = json.dumps(data, indent=4)
        f.write(d)