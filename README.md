# GENDER-DOTS

A challenge set comparing male/female diacritization in Hebrew

# The data

The dataset resides in `data/expected`.

To run the experiment, first clone the repository and `cd` into it.
The files are in `tsv` format (tab-separated values), with the following columns:
* `id`, index of the example in the file
* `bookid`, a unique id for the book (across files)
* `author`, the name of the author of the book (usually in Hebrew)
* `book`, the name of the book (usually in Hebrew)
* `word`, the target word that must be classified correctly (diacritized as male/female)
* `index`, the index of the word in both sentences
* `masculine`, a sentence in which the target word is masculine
* `feminine`, a sentence in which the target word is feminine
* `success_masculine`, 1 if the diacritization of `masculine` is correct, 0 otherwise
* `success_masculine`, 1 if the diacritization of `feminine` is correct, 0 otherwise

## Running the experiment

Then, install the requirements:
```shell
python -m pip install -r requirements.txt
```
