# this is deprecated

from .wiktionaryparser import WiktionaryParser
from bs4 import BeautifulSoup

def fetch(self, word, language=None, old_id=None, proxies={}):
    language = self.language if not language else language
    response = self.session.get(self.url.format(word), params={'oldid': old_id}, proxies=proxies)
    self.soup = BeautifulSoup(response.text.replace('>\n<', '><'), 'html.parser')
    self.current_word = word
    self.clean_html()
    return self.get_word_data(language.lower())

WiktionaryParser.fetch = fetch
