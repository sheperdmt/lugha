from bs4 import BeautifulSoup
import requests
from models.lexicon import Headword
from linguistics import code2name, name2code

proxies = {
    'http': 'socks5://192.168.31.247:9909',
    'https': 'socks5://192.168.31.247:9909',
}

def get_possible_language_list(word):
    url = f"https://en.wiktionary.org/wiki/{word}"
    response = requests.get(url, proxies=proxies)
    if response.status_code == 404:
        h = Headword.new(lemma=word, is_valid=False, langs={})
        h.save()
        return []
    soup = BeautifulSoup(response.text, 'html.parser')
    lang_list = []
    langs = soup.find_all('li', class_='toclevel-1')
    for l in langs:
        lang = l.a['href'].strip('#').replace('_', ' ')
        print('*-*-*-*', lang)
        lang_list.append(name2code(lang))
    return lang_list


if __name__ == '__main__':
    r = get_possible_language_list('the')
    print(r)