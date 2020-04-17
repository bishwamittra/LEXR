import string

import numpy as np
from IPython.display import Image
from IPython.display import display

import graphviz as gv
import functools
import random

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

"""  
Bishwa: The following code uses random with replacement
"""
def bfs_random(alphabet, samplesize):

    nums_of_letters = len(alphabet)
    
    # words=["" for i in range(samplesize)]
    for j in range(samplesize):
        letter=alphabet[np.random.randint(0, nums_of_letters)]
        # letter=random.choices(alphabet,k=samplesize)[j]
        # words[j]+=letter
        yield letter
    # print(words)

if __name__ == "__main__":
    for letter in bfs_random(['a','b'],  100):
        print(letter)
    pass