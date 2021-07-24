from models import Model
from linguistics import name2code, code2name, abbr2pos
from supermemo2 import SMTwo
import time
import datetime
from models.memo import Memopad

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
        return list(self.langs.keys())
    
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
        self.langs[name2code(lang)] = 0
        self.save()

    @classmethod
    def all_possible_langs(cls, lemma):
        h = cls.find_one(lemma=lemma)
        lang_codes = h.possible_langs()
        langs = [code2name(c) for c in lang_codes]
        word_reprs = [f'{lemma}.{c}' for c in lang_codes]
        result = []
        for i in range(len(lang_codes)):
            result.append((lang_codes[i], langs[i], word_reprs[i]))
        return result

    def lang_counter_plus_one(self, lang):
        self.langs[lang] += 1
        self.save()


class Lexis(Model):
    '''
    下面所有类的基类
    '''
    def __init__(self):
        super().__init__()
        self.lemma = ''
        self.lang = ''
        self.etym_no = -1
        self.repr = ''

    @classmethod
    def find_by_repr(cls, repr):
        '''
        根据上下位关系来查找数据
        上下位关系是指：
        词元 lemma
        词 word
        带词性的词 word_by_pos
        义项 sema
        卡片 card
        '''
        attrs_keys = ['lang', 'etym_no', 'pos', 'sema_no']
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
        self.prnn = '' # 读音
        self.word_by_pos_list = []
        self.sema_list = []

    def add_to_counter(self):
        h = Headword.find_or_new(lemma=self.lemma)
        if h.langs.get(self.lang) is None:
            h.langs[self.lang] = 0
        h.lang_counter_plus_one(self.lang)
        h.save()

    def get_semas(self):
        return [Sema.find_by_id(sema_id) for sema_id in self.sema_list]

    @classmethod
    def get_all_semas(cls, lemma):
        words = cls.find(lemma=lemma)
        sema_list = []
        for w in words:
            sema_list += w.get_semas()
        return sema_list

    def get_wbps(self):
        data = []
        for p in self.word_by_pos_list:
            wbp = Word_by_PoS.find_by_id(p)
            semas = wbp.get_semas()
            data.append(dict(
                text=wbp.text,
                pos=abbr2pos(wbp.pos),
                semas=semas,
                ))
        return data

    @classmethod
    def data_for_word_page(cls, lemma, lang):
        data = []
        words = Word.find(lemma=lemma, lang=lang)
        for word in words:
            wbps = word.get_wbps()
            data.append(dict(
                etym=word.etym,
                prnn=word.prnn,
                wbps=wbps,
            ))
        return data


class Word_by_PoS(Lexis):
    '''
    根据词性划分的词条
    '''
    def __init__(self):
        super().__init__()
        self.pos = ''
        self.text = ''
        self.rel = {}
        self.sema_list = []

    def get_semas(self):
        data = []
        for s in self.sema_list:
            sema = Sema.find_by_id(s)
            data.append(sema)
        return data


class Sema(Lexis):
    '''
    义项，根据 sematic 模仿 lemma 生造
    也可以认为来自斯瓦希里语动词 kusema
    '''
    def __init__(self):
        super().__init__()
        self.pos = ''
        self.sema_no = -1
        self.content = ''
        self.examples = []
        self.users = [] # 哪些用户收藏了这个义项

    def delete_sema_user(self, user_id):
        if user_id in self.users:
            self.users.remove(user_id)
        self.save()

    def add_sema_user(self, user_id):
        if user_id not in self.users:
            self.users.append(user_id)
        self.save()

    @classmethod
    def batch_add_sema_user(cls, sema_id_list, user_id):
        for s in sema_id_list:
            sema = Sema.find_by_id(s)
            sema.add_sema_user(user_id)

    @classmethod
    def batch_delete_sema_user(cls, sema_id_list, user_id):
        for s in sema_id_list:
            sema = Sema.find_by_id(s)
            sema.delete_sema_user(user_id)

    def profile(self):
        wbp = self.find_wbp()
        word = self.find_word()
        prfl = dict(
            prnn=word.prnn,
            etym=word.etym,
            text=wbp.text,
        )
        return prfl

    def info(self):
        data = dict(
            lemma=self.lemma,
            lang=self.lang,
            etym_no=self.etym_no,
            pos=self.pos,
            sema_no=self.sema_no,
            sema_id=self.id,
            repr=self.repr
        )
        return data

    def find_wbp(self):
        dict_keys = ['lemma', 'lang', 'etym_no', 'pos']
        d = {}
        for k in dict_keys:
            d[k] = self.__dict__[k]
        wbp = Word_by_PoS.find_one(**d)
        return wbp

    def find_word(self):
        dict_keys = ['lemma', 'lang', 'etym_no']
        d = {}
        for k in dict_keys:
            d[k] = self.__dict__[k]
        word = Word.find_one(**d)
        return word


class Card(Lexis):
    '''
    卡片就是带上用户自定义信息的 sema
    '''
    def __init__(self):
        super().__init__()
        self.memos_list = [] # 一张卡片可以属于多个单词本，记录单词本的memo_no
        self.user_id = -1 # 但是只能属于一个用户
        self.sema_id = -1 # 每张卡对应一个 sema

        self.pos = ''
        self.sema_no = -1

        self.easiness = 0.0 # 下面这四个用于背单词
        self.interval = -1
        self.repetitions = -1
        self.review_time = self.ct

        self.note = '' # 给单词写笔记

    def get_memos_list(self):
        data = []
        for m in self.memos_list:
            memopad = Memopad.find_by_id(m)
            data.append(memopad.get_info())
        return data

    def load_review_date(self):
        d = datetime.date.fromtimestamp(self.review_time)
        return d

    @staticmethod
    def dump_review_date(d):
        t = time.mktime(d.timetuple())
        return t

    def review(self, recall_quality):
        today = datetime.date.today()
        if self.repetitions < 1:
            r = SMTwo.first_review(recall_quality, today)
        else:
            last_review_date = self.load_review_date()
            r = SMTwo(self.easiness, self.interval, self.repetitions, last_review_date)
            r.review(recall_quality, today)
        review_time = self.dump_review_date(r.review_date)
        self.easiness = r.easiness
        self.interval = r.interval
        self.repetitions = r.repetitions
        self.review_time = review_time
        self.save()

    @classmethod
    def remove_user_card(cls, sema_id, user_id):
        sema = Sema.find_by_id(sema_id)
        cards = cls.find_by_repr(sema.repr)
        if len(cards) > 0:
            [card] = [c for c in cards if c.user_id == user_id]
            card.delete()

    @classmethod
    def batch_remove_user_card(cls, sema_id_list, user_id):
        for sema_id in sema_id_list:
            cls.remove_user_card(sema_id, user_id)

    @classmethod
    def new_card(cls, sema_id, user_id):
        sema = Sema.find_by_id(sema_id)
        info = sema.info()
        card = cls.new(**info)
        card.user_id = user_id
        card.save()
        return card

    def add_to_memos_list(self, memo_id):
        if memo_id not in self.memos_list:
            self.memos_list.append(memo_id)
        self.save()

    def delete_from_memos_list(self, memo_id):
        if memo_id in self.memos_list:
            self.memos_list.remove(memo_id)
        self.save()
