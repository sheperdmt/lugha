from models import Model

class Memopad(Model):
    def __init__(self):
        super().__init__()
        self.name = ''
        self.user_id = -1
        self.memo_no = -1 # 即该单词本相对于用户的序号
        self.content = [] # 保存 sema_id，用 sema_id 和 user_id 可以唯一确定卡片
        self.description = ''

    def get_info(self):
        info = self.__dict__.copy()
        info.pop('_id')
        info.pop('deleted')
        info.pop('type')
        return info

    @classmethod
    def get_new_memo_no(cls, user_id):
        memopads_of_the_user = cls.find(user_id=int(user_id))
        memo_no_list = []
        for m in memopads_of_the_user:
            memo_no_list.append(m.memo_no)
        return max(memo_no_list) + 1

    @classmethod
    def add_card_to_multiple_memopads(cls, memo_id_dict, sema_id, user_id):
        from models.lexicon import Card
        card = Card.find_one(sema_id=int(sema_id), user_id=user_id)
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
        card.save()