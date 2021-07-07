import os.path
from bs4 import BeautifulSoup
import requests


def to_filename(s):
    return s.replace('"', '').replace(':', '').replace('?', '').replace('|', 'או').replace('/', ';')


def fetch_text(link):
    page = requests.get(link).text
    soup = BeautifulSoup(page, features='lxml-html')
    for match in soup.find_all('section'):
        match.decompose()
    text = ''
    for article in soup.find_all(lambda tag: tag.name == 'article' and not tag.attrs):
        for match in article.find_all('div'):
            match.decompose()
        text += soup.find('article').get_text()
    if not text.strip():
        return None
    return text


def scrape():
    with open('shortstoryproject-list.tsv', encoding='utf8') as f:
        csv = [line.strip().split('\t') for line in f if line.strip()]

    for i, (title, author, link, tags) in enumerate(csv, 1):
        print(i, title, author, tags, link)

        filename = f'shortstoryproject/{to_filename(author)} - {to_filename(title)}.txt'

        if os.path.exists(filename):
            continue

        text = fetch_text(link)
        if text is None:
            # Premium
            continue

        with open(filename, 'w', encoding='utf8') as f:
            print(text, file=f)
            print(file=f)
            print(link, file=f)
            print(tags, file=f)


if __name__ == '__main__':
    scrape()
