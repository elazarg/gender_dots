import utils
import argparse


def percent(n):
    return round(n * 100, 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print results of tests.')
    parser.add_argument('filenames', metavar='file', type=str, nargs='+',
                        help='names of tsv files')

    args = parser.parse_args()
    for filename in args.filenames:
        rows = list(utils.read_tsv(filename))
        female_success = percent(sum(int(row[-1]) for row in rows) / len(rows))
        male_success = percent(sum(int(row[-2]) for row in rows) / len(rows))

        print(male_success, female_success)
