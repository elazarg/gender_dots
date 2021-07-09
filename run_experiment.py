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


def print_row(system, size, masc, fem):
    if isinstance(masc, str):
        print(f'{system:>13} {size:>5} {masc:>9}  {fem:>9} ratio')
    else:
        print(f'{system:>13} {size:>5} {masc:>9.2%}  {fem:>9.2%} {masc/fem:>5.3}')


def print_results(system, category):
    results_file = make_filename(system, category)
    rows = list(read_tsv(results_file))
    female_success = sum(int(row[-1]) for row in rows) / len(rows)
    male_success = sum(int(row[-2]) for row in rows) / len(rows)
    print_row(category, len(rows), male_success, female_success)


def print_results_original(system, category):
    results_file = make_filename(system, category)
    rows = list(read_tsv(results_file))
    original_success = sum(int(row[-2] if int(row[-3]) == 1 else row[-1]) for row in rows) / len(rows)
    copy_success = sum(int(row[-1] if int(row[-3]) == 1 else row[-2]) for row in rows) / len(rows)
    print_row(category, len(rows), original_success, copy_success)


def print_count_original(system, category):
    results_file = make_filename(system, category)
    rows = list(read_tsv(results_file))
    original_number = sum((1 if int(row[-3]) == 1 else 0) for row in rows)
    copy_number = sum((1 if int(row[-3]) == 2 else 0) for row in rows)
    print(f'{category:>13} {original_number} {copy_number}')


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
    parser.add_argument('--no-classify', action="store_true", default=False)
    parser.add_argument('--original', action="store_true", default=False)
    parser.add_argument('--count', action="store_true", default=False)
    args = parser.parse_args()

    if args.original:
        print_row(args.system, "#", "ORIGNAL (%)", "COPY (%)")
    elif args.count:
        print(args.system, "#ORIGINAL", "#COPY")
    else:
        print_row(args.system, "#", "MASC (%)", "FEM (%)")
    for category in args.category:
        if not args.no_classify:
            run_experiment(args.system, category)
        if args.original:
            print_results_original(args.system, category)
        elif args.count:
            print_count_original(args.system, category)
        else:
            print_results(args.system, category)
