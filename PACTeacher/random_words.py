import string

import numpy as np
from IPython.display import Image
from IPython.display import display

import graphviz as gv
import functools

# from numpy.random._generator import default_rng


def random_word(alphabet):
    nums_of_letters = len(alphabet)
    letter = np.random.randint(0, nums_of_letters)
    word = ""
    while letter != 0:
        word = word + alphabet[letter]
        letter = np.random.randint(0, nums_of_letters)
    return word


def random_word_by_letter(alphabet, p=0.1):
    nums_of_letters = len(alphabet)
    while True:
        if np.random.randint(0, int(1 / p)) == 0:
            break
        letter = np.random.randint(0, nums_of_letters)
        yield alphabet[letter]