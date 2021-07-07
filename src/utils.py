import os
import csv


def iterate_files(base_paths):
    for name in base_paths:
        if not os.path.isdir(name):
            yield name
            continue
        for root, dirs, files in os.walk(name):
            for fname in files:
                path = os.path.join(root, fname)
                yield path


def read_tsv(filename):
    with open(filename, encoding='utf8', newline='') as f:
        yield from csv.reader(f, delimiter='\t')
