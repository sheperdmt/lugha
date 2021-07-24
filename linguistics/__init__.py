import json
import os

PARTS_OF_SPEECH_ABBR = [
    "n", "v", "adj", "adv", "det",
    "art", "prep", "conj", "pr",
    "let", "char", "phr", "prov", "idiom",
    "sym", "syl", "num", "init", "int",
    "def", "pron", "ptc", "pred", "part",
    "suf", "contr",
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
    "suffix", "contraction",
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
        for i in language_list:
            code, canonical_name, family, script = i.split(',', 3)
            codes.append(code)
            canonical_names.append(canonical_name)
            # families.append(family)
            # script = script.strip('"').split(', ')
            # scripts.append(script)
    return codes, canonical_names

def name2code(string):
    codes, canonical_names = generate_languages_data()
    if string[0].isupper():
        d = dict(zip(canonical_names, codes))
        return d[string]
    else:
        return string

def code2name(string):
    codes, canonical_names = generate_languages_data()
    if string[0].islower():
        d = dict(zip(codes, canonical_names))
        return d[string]
    else:
        return string
        
def abbr2pos(abbr):
    d = dict(zip(PARTS_OF_SPEECH_ABBR, PARTS_OF_SPEECH))
    return d.get(abbr)

def pos2abbr(pos):
    d = dict(zip(PARTS_OF_SPEECH, PARTS_OF_SPEECH_ABBR))
    return d.get(pos)

