from collections import Counter
import re
import os.path

import hebrew


def iterate_files(base_paths):
    for name in base_paths:
        if not os.path.isdir(name):
            yield name
            continue
        for root, dirs, files in os.walk(name):
            for fname in files:
                path = os.path.join(root, fname)
                yield path


def shva_for(letter):
    return hebrew.SHVA if letter not in 'אהחע' else hebrew.REDUCED_PATAKH


def add_dagesh(letter):
    if letter in 'אהחער':
        return letter
    if letter[0] == 'ש':
        assert len(letter) == 2
        return letter[0] + hebrew.DAGESH + letter[1]
    return letter + hebrew.DAGESH


def maktel_from_root(root, *, male):
    gender_niqqud = hebrew.SEGOL if male else hebrew.KAMATZ
    if root[0] == 'י':
        MaKTeL = '{mem}{wow}{holam}{r2}{segol_or_kamatz}{h}'
        yield MaKTeL.format(
            mem='מ',
            patakh=hebrew.PATAKH,
            wow='ו',
            holam=hebrew.HOLAM,
            r2=root[1],
            segol_or_kamatz=gender_niqqud,
            h='ה'
        )
    else:
        MaKTeL = '{mem}{patakh}{r1}{shva}{r2}{dagesh_kal}{segol_or_kamatz}{h}'
        yield MaKTeL.format(
            mem='מ',
            patakh=hebrew.PATAKH,
            r1=root[0],
            shva=shva_for(root[0]),
            r2=root[1],
            dagesh_kal=hebrew.DAGESH_LETTER if root[1] in 'בגדכפת' else '',
            segol_or_kamatz=gender_niqqud,
            h='ה'
        )
        MeKaTeL = '{mem}{shva}{r1}{patakh}{r2}{segol_or_kamatz}{h}'
        yield MeKaTeL.format(
            mem='מ',
            patakh=hebrew.PATAKH,
            r1=root[0],
            shva=shva_for(root[0]),
            r2=add_dagesh(root[1]),
            segol_or_kamatz=gender_niqqud,
            h='ה'
        )


def savalta_pattern(male):
    gender_niqqud = hebrew.KAMATZ if male else hebrew.SHVA
    asita = r'{r1}{kamatz}{r2}{patakh}{r3}{shva}{tav}{dagesh}{shva_or_kamatz}'
    letter = '[א-ת]' + r'(?={}|{})?{}?'.format(hebrew.SHIN_SMALIT, hebrew.SHIN_YEMANIT, hebrew.DAGESH)
    return asita.format(
        r1=letter,
        kamatz=hebrew.KAMATZ,
        r2=letter,
        patakh=hebrew.PATAKH,
        r3=letter,
        shva=hebrew.SHVA,
        tav='ת',
        dagesh=hebrew.DAGESH,
        shva_or_kamatz=gender_niqqud,
    )


def saneta_pattern(male):
    gender_niqqud = hebrew.KAMATZ if male else ''
    asita = r'{r1}{kamatz}{r2}{tzere}{aleph}{tav}{kamatz_or_nothing}'
    letter = '[א-ת]' + r'(?:{}|{})?{}?'.format(hebrew.SHIN_SMALIT, hebrew.SHIN_YEMANIT, hebrew.DAGESH)
    return asita.format(
        r1=letter,
        kamatz=hebrew.KAMATZ,
        r2=letter,
        tzere=hebrew.TZEIRE,
        aleph='א',
        tav='ת',
        kamatz_or_nothing=gender_niqqud,
    ) + '(?=[^ִ])'


def hitpaalta_pattern():
    gender_niqqud = hebrew.KAMATZ if male else ''
    asita = r'{r1}{kamatz}{r2}{tzere}{aleph}{tav}{kamatz_or_nothing}'
    letter = '[א-ת]' + r'(?:{}|{})?{}?'.format(hebrew.SHIN_SMALIT, hebrew.SHIN_YEMANIT, hebrew.DAGESH)
    return asita.format(
        r1=letter,
        kamatz=hebrew.KAMATZ,
        r2=letter,
        tzere=hebrew.TZEIRE,
        aleph='א',
        tav='ת',
        kamatz_or_nothing=gender_niqqud,
    ) + '(?=[^ִ])'


def asita_pattern(male):
    # Missing: gilita pattern
    # Missing: Hayita pattern
    gender_niqqud = hebrew.KAMATZ if male else ''
    asita = r'{r1}{kamatz}{r2}{hirik}{yod}{tav}{kamatz_or_nothing}'
    letter = '[א-ת]' + r'(?={}|{})?{}?'.format(hebrew.SHIN_SMALIT, hebrew.SHIN_YEMANIT, hebrew.DAGESH)
    prefixes = '(?:' + '|'.join(['שֶׁ', 'וְשֶׁ', 'כְּשֶׁ', 'לִכְשֶׁ', 'וּכְשֶׁ', 'וְלִכְשֶׁ', 'מִכְּשֶׁ', 'מִשֶּׁ', 'וּמִכְּשֶׁ', '']) + ')?'
    return '[^\u0590-\u05FF]' + prefixes + asita.format(
        r1=letter,
        kamatz=hebrew.KAMATZ,
        r2=letter,
        hirik=hebrew.HIRIK,
        yod='י',
        tav='ת',
        dagesh=hebrew.DAGESH,
        kamatz_or_nothing=gender_niqqud,
    ) + '(?=[^\u0590-\u05FF])'


def hayita_pattern(male):
    if male:
        return 'הָיִיתָ'
    else:
        return 'הָיִית' + '(?=[^\u0590-\u05FF])'


def bata_pattern(male):
    if male:
        return 'בָּאתָ'
    else:
        return 'בָּאת' + '(?=[^\u0590-\u05FF])'


def make_definite(word):
    w, *ord = word
    dagesh = '' if w in 'אהחער' else hebrew.DAGESH
    niqqud = hebrew.PATAKH if w != 'א' else hebrew.KAMATZ
    return niqqud + w + dagesh + ''.join(ord)


def to_regex(word):
    return fr'{word}\b'


with open('../experiments/roots.txt', encoding='utf8') as f:
    roots = [tuple(line.strip().split('\t')[::-1]) for line in f if line.strip()]

bias_words = {}
with open('male_k.txt', encoding='utf8') as f:
    bias_words[True] = {line.strip() for line in f if line.strip()}
with open('female_k.txt', encoding='utf8') as f:
    bias_words[False] = {line.strip() for line in f if line.strip()}

counters = {True: Counter(), False: Counter()}
sufkinds_k = {True: ['ְךָ', 'ֶיךָ'], False: ['ֵךְ', 'ָךְ', 'ַיִךְ']}
sufkinds_t = {True: ['ִיתָ', 'ְתָּ', 'ְתָ'], False: ['ִית', 'ְתְּ', 'ְתְ']}

found_k = {True: set(), False: set()}
found_t = {True: set(), False: set()}

seen = set()


def collect_by_roots(male, text):
    with open('non-maktel-words.txt', encoding='utf8') as f:
        non_words = f.read().strip().split()

    maktels = [m for root in roots for m in maktel_from_root(root, male=male)]
    maktels += [make_definite(word) for word in maktels]
    pat_text = f"(?:{'|'.join(maktels)})"

    pat = re.compile(pat_text)
    full_pat = re.compile(rf'[^.?!]*{pat_text}[^.?!]*?[.?!]')

    sentences = re.findall(full_pat, text)
    for sentence in sentences:
        for nonword in non_words:
            sentence = sentence.replace(nonword, hebrew.remove_niqqud(nonword))
        words = re.findall(pat, sentence)
        found_t[male].update(words)
        n = len(words)
        counters[male]['TAV'] += n
        if n == 1:
            yield sentence, words


def print_suf(male, text):
    with open('non-kaf-words.txt', encoding='utf8') as f:
        non_words = f.read().strip().split()
    for suf in sufkinds_k[male]:
        sentences = re.findall(r'\s[^.?!]*?\b\S*' + suf + r'[^.?!]*?[.?!]', text)
        for sentence in sentences:
            for nonword in non_words:
                sentence = sentence.replace(nonword, hebrew.remove_niqqud(nonword))
            words = re.findall(r'\b\S*' + suf, sentence)
            n = len(words)
            counters[male]['KAF'] += n
            found_k[male].update(words)
            if n == 1:
                yield sentence, words


def print_savalta(male, text):
    with open('non-tav-words.txt', encoding='utf8') as f:
        non_words = f.read().strip().split()
    text.replace(hebrew.DAGESH, '')
    pat = '|'.join([
        # savalta_pattern(male),
        # saneta_pattern(male),
        # asita_pattern(male),
        # hayita_pattern(male)
        bata_pattern(male)
    ])
    pat = f"(?:{pat})"
    sentences = re.findall(rf'[^.?!]*{pat}[^.?!]*?[.?!]', text)
    for sentence in sentences:
        for nonword in non_words:
            sentence = sentence.replace(nonword, hebrew.remove_niqqud(nonword))
        # print(pat)
        words = re.findall(pat, sentence)
        found_t[male].update(words)
        n = len(words)
        counters[male]['TAV'] += n
        if n == 1:
            yield sentence, words


with open('hitpael.txt', encoding='utf8') as f:
    hitpael_words = f.read().strip().split()


def print_hitpael(text):
    text = hebrew.remove_niqqud(text)
    pat = '|'.join(hitpael_words)
    pat = f"(?:{pat})"
    sentences = re.findall(rf'[^.?!]*{pat}[^.?!]*?[.?!]', text)
    for sentence in sentences:
        words = re.findall(pat, sentence)
        n = len(words)
        if n == 1:
            yield sentence, words


with open('paal.txt', encoding='utf8') as f:
    paal_words = f.read().strip().split()


def print_paal(text):
    text = hebrew.remove_niqqud(text)
    pat = '|'.join(paal_words)
    pat = rf"\b(?:{pat})\b"
    sentences = re.findall(rf'[^.?!]*{pat}[^.?!]*?[.?!]', text)
    for sentence in sentences:
        words = re.findall(pat, sentence)
        n = len(words)
        if n == 1:
            yield sentence, words


for i, fname in enumerate(iterate_files(['../../gender_dots/shortstoryproject']), 1):
    basename = os.path.basename(fname).replace('.txt', '')
    # print(i, basename, end='\n', flush=True)
    with open(fname, encoding='utf8') as f:
        text = f.read().replace('\n', ' ')

    for sentence, words in print_hitpael(text):
        print(i, os.path.basename(fname).replace('.txt', ''), '|'.join(sorted(words)), sentence, sep='+')
    if False:
        for male in [True, False]:
            for sentence, words in collect_by_roots(male, text):
                print(i, '|'.join(sorted(words)), os.path.basename(fname).replace('.txt', ''), sentence, sep='+')

            print_suf(male, text)
            for sentence, words in print_savalta(male, text):
                print(i, '|'.join(sorted(words)), os.path.basename(fname).replace('.txt', ''), sentence, sep='+')

# for root in seen:
#     print(maktel_from_root(root, male=True), counters[True][root], counters[False][root])
#
# print('TAV', counters[True]['TAV'], counters[False]['TAV'])
# print(found_t[True])
# print(found_t[False])
#
# print('KAF', counters[True]['KAF'], counters[False]['KAF'])
# print(found_k[True])
# print(found_k[False])
