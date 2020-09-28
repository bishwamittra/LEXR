import numpy as np
import random
import exrex
import rstr
import re
import LTL2DFA as ltlf2dfa
import random
import string
from RNN2DFA.Training_Functions import make_train_set_for_target
import math

# construct a dfa that implements alternating bit protocol


class Alternating_Bit_Protocol:
    def __init__(self):
        self.dfa = ltlf2dfa.DFA()
        self.target_formula = "alternating bit protocol"
        self.construct_dfa()
        self.alphabet = self.dfa.alphabet
        self.classify_word = self.dfa.classify_word

        self.query_formulas = [
            "false",  # rejects everything
            "true",  # accepts everything
            "~F(a)",
            "~F(b)",
            "~F(c)",
            "~F(d)",
            "G(d)",

            "G( (a->F(c)) & (c->F(b)) & (b->F(d)) )",

            "F(a U (b|d)) | F(b U (a|c)) |  F(c U (a|d)) ",
            
            
            "F(a U c) & F(c U b) & F(b U d) ",
            
            "~(F(a U c) & F(c U b) & F(b U d))"
        ]

    def construct_dfa(self):
        # alphabet
        alphabet = "abcd"
        """ 
        a = bit 0 
        b = bit 1
        c = bit 0 acknowledge
        d = bit 1 acknowledge
        """
        self.dfa.alphabet = [character for character in alphabet]
        # state 4 denotes rejecting state for all unalowed move
        self.dfa.Q = [0, 1, 2, 3, 4]
        self.dfa.q0 = 0
        self.dfa.F = [0]
        self.dfa.delta = {
            0: {
                '0001': 0,
                '0010': 4,
                '0100': 4,
                '1000': 1,
                '0000': 0  # implements empty input
            },
            1: {
                '0001': 4,
                '0010': 2,
                '0100': 4,
                '1000': 1,
                '0000': 1  # implements empty input
            },
            2: {
                '0001': 4,
                '0010': 2,
                '0100': 3,
                '1000': 4,
                '0000': 2  # implements empty input
            },
            3: {
                '0001': 0,
                '0010': 4,
                '0100': 3,
                '1000': 4,
                '0000': 3  # implements empty input
            },
            4: {
                '0001': 4,
                '0010': 4,
                '0100': 4,
                '1000': 4,
                '0000': 4  # implements empty input
            }
        }

    def generate_matching_strings(self, n, max_sequence_length=20):

        sequences = []
        for sequence_length in range(4, max_sequence_length+1):
            for i in range(int(n/max_sequence_length-3)):
                _max = np.random.randint(
                    2, max(3, int(math.ceil(sequence_length/4))))
                msg0 = np.random.randint(1, _max)
                ack0 = np.random.randint(1, _max)
                msg1 = np.random.randint(1, _max)
                ack1 = np.random.randint(1, _max)
                init_ack1 = int(ack1/2)
                ack1 = ack1 - init_ack1
                repeatation = np.random.randint(1, max(
                    2, int(math.ceil(sequence_length/(init_ack1 + msg0 + msg1 + ack0 + ack1)))))
                r = '(d{'+str(init_ack1)+'}a{'+str(msg0)+'}c{'+str(ack0) + \
                    '}b{'+str(msg1)+'}d{'+str(ack1) + \
                    '}){' + str(repeatation) + '}'
                sequences.append(exrex.getone(r))
                assert(self.classify_word(
                    sequences[-1])), sequences[-1]+" classification error"

        return sequences


class Email():
    def __init__(self):
        self._at_the_rate = "a"
        self._dot = "d"
        self._numerical_symbols = "m"
        self._letter_symbols = "p"
        self.alphabet = self._at_the_rate + self._dot + \
            self._numerical_symbols + self._letter_symbols
        self._construct_regex()
        self.target_formula = "email match"

        self._numerical_symbols_regex = "|".join(
            [char for char in self._numerical_symbols])
        self._letter_symbols_regex = "|".join(
            [char for char in self._letter_symbols])
        self._all_symbols_regex = "|".join(
            [char for char in self._numerical_symbols+self._letter_symbols])

        self.query_formulas = [
            "false",  # rejects everything
            "true",  # accepts everything
            "(m)",  # email starts with numeric symbols
            "~F(a)",  # there is no '@'
            "~F(d)",  # there is no '.'
            "~F(p)",
            "~F(m)",
            "F(a & X(Fa))",
            "F(d & X(Fd))",
            "F(d & X(Fm))",
            "F(d & X(Gp))",
            "F(a & X(G(~d)))",
            "(~F(m)) & F(p U a) & F(a & X(p U d)) & F(d & X(Gp))",
            "F(a & X(d))",
            "G(m)",  
            "~p",
            "a", 
            "d", 
            "F((p|m) U a) & F(a & X((p|m) U d)) & F(d & X(Gp))",
            
            
            "F(a & X(d))",
            # "~F(a | m)",
            # "~F(d)",  # there is no '.'
            # "~F(a | d | m)",
            # "F(m & X(F(a & X(F(m)))))",
            
        ]

    def _construct_regex(self):
        _only_letter = "("+"|".join(
            char for char in self._letter_symbols)+")"
        _both = "("+"|".join(
            char for char in self._letter_symbols+self._numerical_symbols)+")"

        self.regex = _only_letter + \
            _both + \
            "*" + \
            self._at_the_rate + \
            _both + \
            "+" + \
            self._dot + \
            _only_letter + \
            "+" + \
            "$"
        # print(self.regex)

    def classify_word(self, word):
        return bool(re.match(self.regex, word))
        pass

    def generate_matching_strings(self, n, max_length=20):
        strings = []
        for length in range(5, max_length+1):
            for i in range(int(n/(max_length-4))):
                # print(length)
                prefix_length = random.randint(
                    0, length-5)  # the part before '@'
                # print(prefix_length)
                suffix_length = length-prefix_length-4
                # print(suffix_length)
                suffix_length_1 = random.randint(1, suffix_length)
                suffix_length_2 = suffix_length + 1  - suffix_length_1
                # print(suffix_length_1, suffix_length_2)
                r = "("+self._letter_symbols_regex + \
                    "){1}" + "("+self._all_symbols_regex+")" + \
                    "{" + str(prefix_length) + "}" + self._at_the_rate + "(" + self._all_symbols_regex +\
                    "){" + str(suffix_length_1) + "}"+self._dot +\
                    "(" + self._letter_symbols_regex + \
                    "){" + str(suffix_length_2) + "}"
                strings.append(exrex.getone(r))
                assert(self.classify_word(
                    strings[-1])), strings[-1]+" classification error"
        return strings


class Reber_Grammar:

    def __init__(self):
        self.alphabet = 'BTSXPVE'
        self.target_formula = "reber grammar"
        self._graph = [[(1, 5), ('T', 'P')], [(1, 2), ('S', 'X')],
                       [(3, 5), ('S', 'X')], [(6,), ('E')],
                       [(3, 2), ('V', 'P')], [(4, 5), ('V', 'T')]]

    def classify_word(self, word):

        if len(word) == 0 or word[0] != 'B':
            return False
        node = 0
        for c in word[1:]:
            transitions = self._graph[node]
            try:
                node = transitions[0][transitions[1].index(c)]
                if(node == 6):
                    return True
            except ValueError:  # using exceptions for flow control in python is common
                return False
        return False

    def sequenceToWord(self, sequence):
        """
        converts a sequence (one-hot) in a reber string
        """
        reberString = ''
        for s in sequence:
            index = np.where(s == 1.)[0][0]
            reberString += self.alphabet[index]
        return reberString

    def generateSequences(self, maxLength):
        while True:
            inchars = ['B']
            node = 0
            while node != 6:
                transitions = self._graph[node]
                i = np.random.randint(0, len(transitions[0]))
                inchars.append(transitions[1][i])
                node = transitions[0][i]
            if len(inchars) < maxLength:
                return inchars

    def get_one_example(self, maxLength):
        inchars = self.generateSequences(maxLength)
        inseq = []
        for i in zip(inchars):
            inpt = np.zeros(7)
            inpt[self.alphabet.find(i[0])] = 1.
            inseq.append(inpt)
        seq = inseq
        outseq = inseq[1:]
        inseq = inseq[0:-1]
        return seq, inseq, outseq


class Balanced_Parentheses:

    """  
    There are reserved letters.
    '(' = l
    ')' = r
    Therfore, bp_other_letters cannot contain l and r.
    """

    def __init__(self):
        self._bp_other_letters = "a"
        self.alphabet = "lr" + self._bp_other_letters
        self.target_formula = "balanced parentheses"

        self.query_formulas = [
            "false",  
            "true",
            "~F(l|r)", 
            "G(l -> F(r))",
            "G(l -> ~(F(r)))",
            "G(l -> F(a | r))",
            "G(l -> ~(F(a | r)))",
            "G(a)",
            "r",  # starts with right parenthesis
            "a U r", 
            "F(l & X(G(~r)))",
            "G(l)",
            "F(l) & F(r) & F( (l|a) U r )",
            "F(l) & F(r) & ~(F( (l|a) U r ))"
        ]

    def _make_similar(self, w, alphabet):
        new = list(w)
        indexes = list(range(len(new)))
        # switch characters
        num_switches = random.choice(range(3))
        random.shuffle(indexes)
        indexes_to_switch = indexes[:num_switches]
        for i in indexes_to_switch:
            new[i] = random.choice(alphabet)
        # insert characters
        num_inserts = random.choice(range(3))
        indexes = indexes + [len(new)]
        indexes_to_insert = indexes[:num_inserts]
        for i in indexes_to_insert:
            new = new[:i] + [random.choice(alphabet)] + new[i:]
        num_changes = num_switches + num_inserts
        # duplicate letters
        while ((num_changes == 0) or (random.choice(range(3)) == 0)) and len(new) > 0:
            index = random.choice(range(len(new)))
            new = new[:index + 1] + new[index:]
            num_changes += 1
        # omissions
        while ((num_changes == 0) or random.choice(range(3)) == 0) and len(new) > 0:
            index = random.choice(range(len(new)))
            new = new[:index] + new[index + 1:]
            num_changes += 1
        return ''.join(new)

    def classify_word(self, w):
        open_counter = 0
        while len(w) > 0:
            c = w[0]
            w = w[1:]
            if c == "l":
                open_counter += 1
            elif c == "r":
                open_counter -= 1
                if open_counter < 0:
                    return False
        return open_counter == 0

    def _random_balanced_word(self, start_closing):
        count = 0
        word = ""
        while len(word) < start_closing:
            paran = (random.choice(range(3)) == 0)
            next_letter = random.choice(
                "lr") if paran else random.choice(self._bp_other_letters)
            if next_letter == "r" and count <= 0:
                continue
            word += next_letter
            if next_letter == "l":
                count += 1
            if next_letter == "r":
                count -= 1
        while True:
            paran = (random.choice(range(3)) == 0)
            next_letter = random.choice(
                "r") if paran else random.choice(self._bp_other_letters)
            if next_letter == "r":
                count -= 1
                if count < 0:
                    break
            word += next_letter
        return word

    def _n_balanced_words_around_lengths(self, n, short, longg):
        words = set()
        while len(words) < n:
            for l in range(short, longg):
                words.add(self._random_balanced_word(l))
    #     print('\n'.join(sorted(list(words),key=len)))
        return words

    # eg 15000, 2, 30
    def get_balanced_parantheses_train_set(self, n, short, longg, lengths=None, max_train_samples_per_length=300, search_size_per_length=200):
        balanced_words = list(
            self._n_balanced_words_around_lengths(n, short, longg))
        almost_balanced = [self._make_similar(
            w, self.alphabet) for w in balanced_words][:int(2*n/3)]
        less_balanced = [self._make_similar(
            w, self.alphabet) for w in almost_balanced]
        barely_balanced = [self._make_similar(
            w, self.alphabet) for w in less_balanced]

        all_words = balanced_words + almost_balanced + less_balanced + barely_balanced
        return make_train_set_for_target(self.classify_word, self.alphabet, lengths=lengths,
                                         max_train_samples_per_length=max_train_samples_per_length,
                                         search_size_per_length=search_size_per_length,
                                         provided_examples=all_words)


import pandas as pd
class DNA_Sequence():
    def __init__(self):
        self.target_formula = "DNA sequence"
        self.alphabet = 'GTACN'
        self.query_formulas = [

        ]

    def get_dict(self, target_class=6):
        df = pd.read_table('benchmarks/raw/dog_data.txt')
        mask = df['class'] != target_class
        df.loc[mask, 'class'] = 'negative'
        mask = df['class'] == target_class
        df.loc[mask, 'class'] = 'positive'
        df['class'] = df['class'].map({"negative" : False, 'positive' : True})
        return pd.Series(df['class'].values,index=df['sequence']).to_dict()

from keras.preprocessing.text import Tokenizer
from keras.preprocessing import sequence
from sklearn.preprocessing import LabelEncoder
class Text_Classification():
    def __init__(self, max_words = 20, max_len = 15):
        self.target_formula = "Text classification"
        self.alphabet = [i for i in range(max_words + 1)]
        self.query_formulas = [
        ]
        self._max_words = max_words
        self._max_len = max_len


        df = pd.read_csv('benchmarks/raw/spam.csv',delimiter=',',encoding='latin-1')
        df = df[['v1', 'v2']]
        df.rename(columns = {'v1' : 'target', 'v2' : 'text'}, inplace=True)
        # print(df.head())
        

        le = LabelEncoder()
        Y = le.fit_transform(df['target'])
        Y = Y.reshape(-1,1)
        
        # tokenize
        tok = Tokenizer(num_words=self._max_words)
        tok.fit_on_texts(df['text'])
        sequences = tok.texts_to_sequences(df['text'])
        sequences_matrix = sequence.pad_sequences(sequences,maxlen=self._max_len)
        # print(sequences_matrix, Y)
        self.dict = {}
        for A, B in zip(sequences_matrix, Y):
            # print(tuple(A),B[0] == 1)
            self.dict[tuple(A)] = B[0] == 1

    def classify_word(self, w):
        w = tuple(w)
        if(w not in self.dict):
            raise ValueError("word not in the original file")
        else:
            return self.dict[w]
        

class Example:
    def __init__(self, alphabet, target_formula, token):
        self.alphabet = alphabet
        self.target_formula = target_formula
        self.dfa = ltlf2dfa.translate_ltl2dfa(
            alphabet=[character for character in self.alphabet], formula=self.target_formula, token=str(token))
        self.classify_word = self.dfa.classify_word


class Example1(Example):

    def __init__(self, token=""):
        super().__init__(alphabet="abc", target_formula="G(~a)", token=token)

        self.query_formulas = [
            "true",
            "false",
            "a",
            "~a",
            'F(a)',
            "F(~a)",
            "F(b)",
            "F(b|c)",
            "G(b|c)",
            'X(G(~a))',
            'X(G(a))'
        ]


class Example2(Example):

    def __init__(self, token=""):
        super().__init__(alphabet="abc", target_formula="G(a->X(b))", token=token)

        self.query_formulas = [
            "true",
            "false",
            "b",
            "X(b)",
            "G(b)",
            "F(a)",
            "G(a)",
        ]


class Example3(Example):

    def __init__(self, token=""):
        super().__init__(alphabet="abc", target_formula="G(b -> G(~a))", token=token)

        self.query_formulas = [
            "true",
            "false",
            'G(b)',
            'G(~a)',
            'G(a)',
            'F(c)'
        ]


class Example4(Example):

    def __init__(self, token=""):
        super().__init__(alphabet=['a', 'b', 'c'], target_formula="F(a)", token=token)

        self.query_formulas = [
            "true",
            "false",
            "F(b)",
            "F(~a)",
            "F(~b)",
            'F(aUb)',
            'F(bUa)',
            "G(a)",
            "G(c)",
            "F(c)",
            "F(a & X(b))"
        ]


class Example5(Example):

    def __init__(self, token=""):
        super().__init__(alphabet="abc", target_formula="F(aUb)", token=token)

        self.query_formulas = [
            "true",
            "false",
            "F(a)",
            "F(aUb)",
            "F(bUa)",
            "G(a)",
            "G(c)",
            "F(c)",
            "F(a & X(b))"
        ]


class Example6(Example):

    def __init__(self, token=""):
        super().__init__(alphabet="abc", target_formula="F(a & X(b))", token=token)

        self.query_formulas = [
            "true",
            "false",
            "F(a)",
            "F(b)",
            "F(c)",
            "G(a)",
            "F(aUb)"
        ]


class Example7(Example):

    def __init__(self, token=""):
        super().__init__(alphabet="abc", target_formula="G(a)", token=token)

        self.query_formulas = [
            "true",
            "false",
            "F(a)",
            "F(b)",
            "F(a|b)",
            "F(aUb)"
        ]


class Example8(Example):

    def __init__(self, token=""):
        super().__init__(alphabet="abc", target_formula="F(b) -> (a U b)", token=token)

        self.query_formulas = [
            "true",
            "false"
        ]


class Example9(Example):

    def __init__(self, token=""):
        super().__init__(alphabet="abc", target_formula="(G(a -> (Xb))) & (G((Xb) -> a))", token=token)

        self.query_formulas = [
            "true",
            "false",
        ]
