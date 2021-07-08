# GENDER-DOTS

A challenge set comparing male/female diacritization in Hebrew

# The data

The dataset resides in `data/expected`.

The files are in `tsv` format (tab-separated values), with the following columns:
* `id`, index of the example in the file
* `bookid`, a unique id for the book (across files)
* `word`, the target word that must be classified correctly (diacritized as male/female)
* `author`, the name of the author of the book (usually in Hebrew)
* `book`, the name of the book (usually in Hebrew)
* `index`, the index of the word in both sentences
* `masculine`, a sentence in which the target word is masculine
* `feminine`, a sentence in which the target word is feminine
* `original`, a number indicating whether the target word in the original sentence is masculine (1) or feminine (2)

The predictions reside in `data/[system]`, for example `data/Dicta`.
In addition to the above columns, the prediction files have two new columns:
* `success_masculine`, 1 if the diacritization of `masculine` is correct, 0 otherwise
* `success_feminine`, 1 if the diacritization of `feminine` is correct, 0 otherwise

## Running the experiment
To run the experiment, first clone the repository and `cd` into it.
Then, install the requirements:
```shell
python -m pip install -r requirements.txt
```

Diacritize using Dicta:
```shell
python run_experiments.py Dicta
```

You can choose which tests to run:
```shell
python run_experiments.py Dicta KAF TAV-PAAL
```

In order to run the Nakdimon test, you first have to run the Nakdimon server, 
available [here](https://github.com/elazarg/nakdimon), on your local machine. 

Morfix prohibit using automated tools for diacritization, so to run them you must use the online GUI: https://nakdan.morfix.co.il/nikud/Demo