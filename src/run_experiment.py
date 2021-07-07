from pathlib import Path

from hebrew import remove_niqqud

import external_apis
import utils


def run_experiment(filename, system):
    fetch = external_apis.SYSTEMS[system]

    lines = list(utils.read_tsv(f'data/expected/{filename}.tsv'))

    outfile = f'data/{system}/{filename}.tsv'

    Path(outfile).parent.mkdir(parents=True, exist_ok=True)

    with open(outfile, 'w', encoding='utf8') as f:
        for i, bookid, author, book, word, index, expected_male, expected_female, original in lines:
            index = int(index)

            actual_male = fetch(remove_niqqud(expected_male))
            actual_female = fetch(remove_niqqud(expected_female))

            success_male = int(expected_male.split()[index] == actual_male.split()[index])
            success_female = int(expected_female.split()[index] == actual_female.split()[index])

            print(i, bookid, author, book, word, index, actual_male, actual_female, original, success_male, success_female,
                  file=f, sep='\t')


if __name__ == '__main__':
    run_experiment('artificial-occupations', 'Dicta')
