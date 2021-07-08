import re

SHVA = '\u05B0'
REDUCED_SEGOL = '\u05B1'
REDUCED_PATAKH = '\u05B2'
REDUCED_KAMATZ = '\u05B3'
HIRIK = '\u05B4'
TZEIRE = '\u05B5'
SEGOL = '\u05B6'
PATAKH = '\u05B7'
KAMATZ = '\u05B8'
HOLAM = '\u05B9'
KUBUTZ = '\u05BB'
SHURUK = '\u05BC'
METEG = '\u05BD'
SHIN_YEMANIT = '\u05c1'
SHIN_SMALIT = '\u05c2'
DAGESH = '\u05bc'


def remove_niqqud(text: str) -> str:
    return re.sub('[\u05B0-\u05BC\u05C1\u05C2ׇ\u05c7]', '', text)


def to_cjrl(text: str) -> str:
    shin = {
        'שּׁ': '+s*',
        'שּׂ': ',s*',
        'שׁ': '+s',
        'שׂ': ',s'
    }

    pairs = {
        'ו' + HOLAM: 'O',
        'ו' + SHURUK: 'U',
    }

    consonants = {
        'א': "'",
        'ב': "b",
        'ג': "g",
        'ד': "d",
        'ה': "h",
        'ו': "w",
        'ז': "z",
        'ח': ".h",
        'ט': ".t",
        'י': "y",
        'כ': "k",
        'ך': "K",
        'ל': "l",
        'מ': "m",
        'ם': "M",
        'נ': "n",
        'ן': "N",
        'ס': "s",
        'ע': "`",
        'פ': "p",
        'ף': "P",
        'צ': ".s",
        'ץ': ".S",
        'ק': "q",
        'ר': "r",
        'ש': '/s',
        'ת': 't',
    }

    vowels = {
        HIRIK: 'i',
        TZEIRE: 'e',
        SEGOL: 'E',
        REDUCED_SEGOL: 'E:',
        PATAKH: 'a',
        REDUCED_PATAKH: 'a:',
        KAMATZ: 'A',
        REDUCED_KAMATZ: 'A:',
        HOLAM: 'o',
        SHURUK: 'u',
        DAGESH: '*',
        SHVA: ':',
    }

    for group in [shin, pairs, consonants, vowels]:
        for c, v in group.items():
            text = text.replace(c, v)
    return text


if __name__ == '__main__':
    text = 'הַמַּרְצֶה עֲשִׁירָה.'
    print(to_cjrl(text))
