from models import Model
from linguistics import code_lang_normalizer, to_canonical_names


class Headword(Model):
    '''
    用来存放一个 Headword 包括哪几种语言，每种有几个 word 的计数器
    '''
    def __init__(self):
        super().__init__()
        self.lemma = ''
        self.langs = {}
        self.is_valid = True

    def valid_langs(self):
        valid_langs = []
        for k, v in self.langs.items():
            if v > 0:
                valid_langs.append(k)
        return valid_langs

    def first_valid_lang(self):
        l = self.valid_langs()
        if len(l) > 0:
            return l[0]
        else:
            return None

    def possible_langs(self):
        return self.langs.keys()
    
    @classmethod
    def does_word_exist(cls, word):
        h = cls.find_one(lemma=word)
        if h is None:
            return False
        langs = h.valid_langs()
        if langs == []:
            return False
        return True

    @classmethod
    def is_word_valid(cls, word):
        h = cls.find_one(lemma=word)
        return h.is_valid 

    def add_possible_lang(self, lang):
        self.langs[code_lang_normalizer(lang)] = 0
        self.save()


class Lexis(Model):
    '''
    下面所有类的基类
    '''
    def __init__(self):
        super().__init__()
        self.lemma = ''
        self.lang = ''
        self.etym_id = -1
        self.repr = ''

    @classmethod
    def find_by_repr(cls, repr):
        attrs_keys = ['lang', 'etym_id', 'pos', 'sema_id']
        attrs_types = [str, int, str, int]
        _lemma, attrs = repr.split('>.')
        lemma = _lemma.strip('<')
        attrs_values = attrs.split('.')
        attrs_values = [attrs_types[i](attrs_values[i]) for i in range(len(attrs_values))]
        attrs_dict = dict(zip(attrs_keys, attrs_values))
        return cls.find(lemma=lemma, **attrs_dict)


class Word(Lexis):
    '''
    根据词源划分的词条
    '''
    def __init__(self):
        super().__init__()
        self.etym = ''
        self.prnn = ''

    def add_to_counter(self):
        h = Headword.find_or_new(lemma=self.lemma)
        if h.langs.get(self.lang) is None:
            h.langs[self.lang] = 0
        h.langs[self.lang] += 1
        h.save()


class Word_by_PoS(Lexis):
    '''
    根据词性划分的词条
    '''
    def __init__(self):
        super().__init__()
        self.pos = ''
        self.text = ''
        self.rel = {}


class Sema(Lexis):
    '''
    义项
    '''
    def __init__(self):
        super().__init__()
        self.pos = ''
        self.sema_id = -1
        self.content = ''
        self.examples = []