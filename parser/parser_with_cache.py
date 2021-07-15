# use this when proxy not needed
# from .wiktionaryparser import WiktionaryParser
# else:
from .wiktionaryparser import WiktionaryParser
from bs4 import BeautifulSoup


def cache_exists(word):
    import os
    path = f'./cached/{word}.html'
    if os.path.exists(path):
        print('***something wrong in cached***')
        return True
    else:
        return False

def get_html_doc(self, word, old_id=None, proxies={}):
    if cache_exists(word):
        with open(f'./cached/{word}.html', 'r') as f:
            return f.read()
    else:
        print('***something wrong in get_html_doc***')
        print("self.url.format(word)", self.url.format(word))
        print('*** proxies ***', proxies)
        response = self.session.get(self.url.format(word), params={'oldid': old_id}, proxies=proxies)
        print('***something wrong in get_html_doc, not getting response?***')
        with open(f'./cached/{word}.html', 'w') as f:
            f.write(response.text)
        print('***something wrong in get_html_doc, not writing document?***')
        return response.text

def fetch(self, word, language=None, old_id=None, proxies={}):
    language = self.language if not language else language
    html_doc = self.get_html_doc(word, proxies=proxies)
    self.soup = BeautifulSoup(html_doc.replace('>\n<', '><'), 'html.parser')
    self.current_word = word
    self.clean_html()
    return self.get_word_data(language.lower())

WiktionaryParser.get_html_doc = get_html_doc
WiktionaryParser.fetch = fetch
