import json
import os

PARTS_OF_SPEECH_ABBR = [
    "n", "v", "adj", "adv", "det",
    "art", "prep", "conj", "pr",
    "let", "char", "phr", "prov", "idiom",
    "sym", "syl", "num", "init", "int",
    "def", "pron", "ptc", "pred", "part",
    "suf",
]

RELATIONS_ABBR = [
    "syn", "ant", "hyper", "hypo",
    "mero", "holo", "tropo", "rel",
    "coor",
]

PARTS_OF_SPEECH = [
    "noun", "verb", "adjective", "adverb", "determiner",
    "article", "preposition", "conjunction", "proper noun",
    "letter", "character", "phrase", "proverb", "idiom",
    "symbol", "syllable", "numeral", "initialism", "interjection",
    "definitions", "pronoun", "particle", "predicative", "participle",
    "suffix",
]

RELATIONS = [
    "synonyms", "antonyms", "hypernyms", "hyponyms",
    "meronyms", "holonyms", "troponyms", "related terms",
    "coordinate terms",
]

def generate_languages_data():
    path = os.getcwd()
    with open(path + '/linguistics/wiktionary_languages.csv', 'r') as f:
        data = f.read()
        codes = []
        canonical_names = []
        families = []
        scripts = []
        language_list = data.split('\n')
        print(language_list[:10])
        for i in language_list:
            code, canonical_name, family, script = i.split(',', 3)
            codes.append(code)
            canonical_names.append(canonical_name)
            # families.append(family)
            # script = script.strip('"').split(', ')
            # scripts.append(script)
    return codes, canonical_names

def code_lang_normalizer(string):
    codes, canonical_names = generate_languages_data()
    if string[0].isupper():
        d = dict(zip(canonical_names, codes))
        return d[string]
    else:
        return string

def to_canonical_names(string):
    codes, canonical_names = generate_languages_data()
    if string[0].islower():
        d = dict(zip(codes, canonical_names))
        return d[string]
    else:
        return string