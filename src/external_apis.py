import re
import json
from functools import wraps

import requests
from cachier import cachier

import hebrew


def split_by_length(characters, maxlen: int):
    assert maxlen > 1
    out = []
    space = maxlen
    for c in characters:
        if c == ' ':
            space = len(out)
        out.append(c)
        if len(out) == maxlen - 1:
            yield out[:space+1]
            out = out[space+1:]
    if out:
        yield out


def piecewise(maxlen):
    def inner(fetch):
        @wraps(fetch)
        def fetcher(text):
            return ' '.join(fetch(''.join(chunk).strip()) for chunk in split_by_length(text, maxlen))
        return fetcher
    return inner


@cachier()
@piecewise(100)
def fetch_morfix(text: str) -> str:
    url = 'https://nakdan.morfix.co.il/nikud/NikudText'

    payload = {
        "text": text,
        "isLogged": 'false',
    }
    headers = {
    }

    r = requests.post(url, data=payload, headers=headers)
    r.raise_for_status()
    return json.loads(r.json()['nikud'])['OutputText']


@cachier()
@piecewise(10000)
def fetch_dicta(text: str) -> str:
    def extract_word(k):
        if k['options']:
            res = k['options'][0][0]
            res = res.replace('|', '')
            res = res.replace(hebrew.KUBUTZ + 'ו' + hebrew.METEG, 'ו' + hebrew.SHURUK)
            res = res.replace(hebrew.HOLAM + 'ו' + hebrew.METEG, 'ו' + hebrew.HOLAM)
            res = res.replace(hebrew.METEG, '')

            res = re.sub(hebrew.KAMATZ + 'ו' + '(?=[א-ת])', 'ו' + hebrew.HOLAM, res)
            res = res.replace(hebrew.REDUCED_KAMATZ + 'ו', 'ו' + hebrew.HOLAM)

            return res
        return k['word']

    url = 'https://nakdan-2-0.loadbalancer.dicta.org.il/api'

    payload = {
        "task": "nakdan",
        "genre": "modern",
        "data": text,
        "addmorph": True,
        "keepqq": False,
        "nodageshdefmem": False,
        "patachma": False,
        "keepmetagim": True,
    }
    headers = {
        'content-type': 'text/plain;charset=UTF-8'
    }

    r = requests.post(url, json=payload, headers=headers)
    r.raise_for_status()
    result = ''.join(extract_word(k) for k in r.json())
    if len(hebrew.remove_niqqud(result)) * 1.2 > len(result):
        print("Failed to dot")
        raise requests.RequestException("Undotted response")
    return result


@cachier()
@piecewise(10000)
def fetch_nakdimon(text: str) -> str:
    url = 'http://127.0.0.1:5000'

    payload = {
        "text": text,
        "model_name": 'final_model/final.h5'
    }
    headers = {
    }

    r = requests.post(url, data=payload, headers=headers)
    r.raise_for_status()
    return r.text


SYSTEMS = {
    'Morfix': fetch_morfix,  # terms-of-use issue
    'Dicta': fetch_dicta,
    'Nakdimon': fetch_nakdimon,
}

# fetch_nakdimon.clear_cache()
# fetch_dicta.clear_cache()
