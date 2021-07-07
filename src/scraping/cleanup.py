import hebrew
import string

with open('artificial-occupations.tsv', encoding='utf8') as f:
    lines = f.read().strip().split('\n')
    lines = [line.split('\t') for line in lines]

for i, bookid, author, book, word, male, female, original in lines:
    word = hebrew.remove_niqqud(word)
    male_clean = hebrew.remove_niqqud(male)
    indices = {n for n, token in enumerate(male_clean.split()) if token.strip(string.punctuation).endswith(word)}
    assert len(indices) == 1, male_clean
    n = indices.pop()

    female_clean = hebrew.remove_niqqud(female)
    indices = {n for n, token in enumerate(female_clean.split()) if token.strip(string.punctuation).endswith(word)}
    assert(len(indices) == 1)
    k = indices.pop()
    assert k == n
    print(i, bookid, hebrew.remove_niqqud(word), author, book, n, male, female, original, sep='\t')
