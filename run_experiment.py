import argparse
from pathlib import Path
import csv

from hebrew import remove_niqqud
import external_apis


def read_tsv(filename):
    with open(filename, encoding='utf8', newline='') as f:
        yield from csv.reader(f, delimiter='\t')


def make_filename(system, category):
    return f'data/{system}/{category}.tsv'


def run_experiment(system, category):
    fetch = external_apis.SYSTEMS[system]

    rows = list(read_tsv(make_filename('expected', category)))

    results_file = make_filename(system, category)

    Path(results_file).parent.mkdir(parents=True, exist_ok=True)

    with open(results_file, 'w', encoding='utf8') as f:
        for i, bookid, author, book, word, index, expected_male, expected_female, original in rows:
            index = int(index)

            actual_male = fetch(remove_niqqud(expected_male))
            actual_female = fetch(remove_niqqud(expected_female))

            success_male = int(expected_male.split()[index] == actual_male.split()[index])
            success_female = int(expected_female.split()[index] == actual_female.split()[index])

            print(i, bookid, author, book, word, index,
                  actual_male, actual_female, original,
                  success_male, success_female,
                  file=f, sep='\t')


def percent(n):
    return round(n * 100, 2)


def print_results(system, category):
    results_file = make_filename(system, category)
    rows = list(read_tsv(results_file))
    female_success = percent(sum(int(row[-1]) for row in rows) / len(rows))
    male_success = percent(sum(int(row[-2]) for row in rows) / len(rows))
    print('\t', category, male_success, female_success)


if __name__ == '__main__':
    categories = ['ART-OCC', 'ART-VERBS', 'KAF', 'NLY-HITPAEL', 'NLY-PAAL', 'NLY-PIEL', 'TAV-PAAL']

    parser = argparse.ArgumentParser(description='Run diacritization tests.')
    parser.add_argument('system', metavar='system', type=str, nargs='?', default='Dicta',
                        choices=['Dicta', 'Nakdimon'],
                        help='Diacritization system.')
    parser.add_argument('category', metavar='category', type=str, nargs='+',
                        default=categories,
                        choices=categories,
                        help='Tests to run')
    args = parser.parse_args()

    print(f'{args.system}:')
    for category in args.category:
        run_experiment(args.system, category)
        print_results(args.system, category)
