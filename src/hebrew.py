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
