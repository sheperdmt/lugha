from bs4 import BeautifulSoup
import requests
from models.lexicon import Headword
from linguistics import name2code

from parser.parser_with_cache import cache_exists

def get_possible_language_list(word):
    if globals().get('__builtins__').get('__debug__'):
        from parser.proxies import proxies
    else:
        proxies = {}
    html_doc = ''
    if cache_exists(word):
        with open(f'./cached/{word}.html', 'r') as f:
            html_doc = f.read()
    else:
        url = f"https://en.wiktionary.org/wiki/{word}?printable=yes"
        response = requests.get(url, proxies=proxies)
        if response.status_code == 404:
            h = Headword.new(lemma=word, is_valid=False, langs={})
            h.save()
            return []
        with open(f'./cached/{word}.html', 'w') as f:
            f.write(response.text)
        html_doc = response.text
    soup = BeautifulSoup(html_doc, 'html.parser')
    lang_list = []
    langs = soup.find_all('li', class_='toclevel-1')
    for l in langs:
        lang = l.a['href'].strip('#').replace('_', ' ')
        # print('*-*-*-*', lang)
        lang_list.append(name2code(lang))
    return lang_list


if __name__ == '__main__':
    r = get_possible_language_list('the')
    print(r)