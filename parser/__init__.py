from .parser_with_cache import WiktionaryParser
from models.lexicon import Headword, Word, Word_by_PoS, Sema
from linguistics import *
import json

parser = WiktionaryParser()

def get_page(word, language):
    language = code2name(language)
    proxies = {}
    if globals().get('__builtins__').get('__debug__'):
        from parser.proxies import proxies
    data = parser.fetch(word, language=language, proxies=proxies)
    return data


pos_dict = dict(zip(PARTS_OF_SPEECH, PARTS_OF_SPEECH_ABBR))
rel_dict = dict(zip(RELATIONS, RELATIONS_ABBR))

the_six_lang_codes = ['en', 'fr', 'de', 'it', 'es', 'la']
# the_six_langs = ['English', 'French', 'German', 'Italian', 'Spanish', 'Latin']


def word_constructor(lemma, lang, etym_no, w):
    word_repr = '<{}>.{}.{}'
    repr = word_repr.format(lemma, lang, etym_no)
    form = dict(
        lemma=lemma,
        lang=lang,
        etym_no=etym_no,
        repr=repr,
        etym=w['etymology'],
        prnn='\n'.join(w['pronunciations']['text']),
    )
    word = Word.new(form)
    word.add_to_counter()
    return word


def word_by_pos_constructor(word, wbp):
    word_by_pos_repr = '<{}>.{}.{}.{}'
    pos = wbp['partOfSpeech']
    if pos != '':
        pos = pos_dict[pos]
    repr = word_by_pos_repr.format(
        word.lemma, word.lang, word.etym_no, pos
    )
    rel = {}
    for r in wbp['relatedWords']:
        rel_type = rel_dict[r['relationshipType']]
        rel[rel_type] = r['words']
    form = dict(
        lemma=word.lemma,
        lang=word.lang,
        etym_no=word.etym_no,
        pos=pos,
        repr=repr,
        text=wbp['text'][0],
        rel=rel,
    )
    word_by_pos = Word_by_PoS.new(form)
    return word_by_pos


def word_into_model(word_name, language, word_data):
    sema_repr = '<{}>.{}.{}.{}.{}'
    lang = name2code(language)
    count = 0
    for w in word_data:
        count += 1
        word = word_constructor(word_name, lang, count, w)
        for wbp in w['definitions']:
            word_by_pos = word_by_pos_constructor(word, wbp)
            for i in wbp['text'][1]:
                repr = sema_repr.format(
                    word.lemma, word.lang, word.etym_no, word_by_pos.pos, i
                )
                content = wbp['text'][1][int(i)]
                examples = wbp['examples'][int(i)]
                form = dict(
                    lemma=word.lemma,
                    lang=word.lang,
                    etym_no=word.etym_no,
                    pos=word_by_pos.pos,
                    sema_no=int(i),
                    repr=repr,
                    content=content,
                    examples=examples,
                )
                sema = Sema.new(form)
                sema.save()
                word_by_pos.sema_list.append(sema.id)
                word.sema_list.append(sema.id)
            word_by_pos.save()
            word.word_by_pos_list.append(word_by_pos.id)
        word.save()


def run(word_name, language):
    data = get_page(word_name, language)
    word_into_model(word_name, language, data)


def initialize_new_headword(word, possible_language_list):    
    any_of_the_six = []
    for lang in possible_language_list:
        headword = Headword.find_or_new(lemma=word)
        headword.add_possible_lang(lang)
        if lang in the_six_lang_codes:
            data = get_page(word, code2name(lang))
            word_into_model(word, lang, data)
            any_of_the_six.append(lang)
    if any_of_the_six != []:
        return any_of_the_six[0]
    else:
        return None


def test(word_name, language):
    data = get_page(word_name, language)
    word_into_model(word_name, language, data)
    with open(f'./temp/{word_name}-{language}.txt', 'w', encoding='utf-8') as f:
        d = json.dumps(data, indent=4)
        f.write(d)