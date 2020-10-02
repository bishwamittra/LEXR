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
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# construct a dfa that implements alternating bit protocol


class Alternating_Bit_Protocol:
    def __init__(self,token=""):
        self.dfa = ltlf2dfa.DFA()
        self.target_formula = "alternating bit protocol"
        self.construct_dfa()
        self.alphabet = self.dfa.alphabet
        self.classify_word = self.dfa.classify_word

        """ 
        a = bit 0 
        b = bit 1
        c = bit 0 acknowledge
        d = bit 1 acknowledge
        """
        

        self._query_formulas = [
            "false",  # rejects everything
            "true",  # accepts everything
            "!(F(a))",
            "!(F(b))",
            "!(F(c))",
            "!(F(d))",
            "G(d)",

            "G(&(&(->(a,F(c)),->(c,F(b))),->(b,F(d))))",

            "|(|(F(U(a,|(b,d))),F(U(b,|(a,c)))),F(U(c,|(a,d))))",
            
            
            "&(&(F(U(a,c)),F(U(c,b))),F(U(b,d)))",
            
            "!(&(&(F(U(a,c)),F(U(c,b))),F(U(b,d))))",
            
        ]

        dic = {
            "a" : "x0",
            "b" : "x1",
            "c" : "x2",
            "d" : "x3"
        }
        
        self.query_formulas = []
        for formula in self._query_formulas:
            if(formula != "false"):
                for key in dic:
                    formula = formula.replace(key, dic[key])
            self.query_formulas.append(formula)

        # print(self.query_formulas)

    def construct_dfa(self):
        # alphabet
        self.dfa.alphabet = ['x0', 'x1', 'x2', 'x3']
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
                r = '((x3){'+str(init_ack1)+'}(x0){'+str(msg0)+'}(x2){'+str(ack0) + \
                    '}(x1){'+str(msg1)+'}(x3){'+str(ack1) + \
                    '}){' + str(repeatation) + '}'
                sequences.append(exrex.getone(r))
                assert(self.classify_word(
                    sequences[-1])), sequences[-1]+" classification error"

        return sequences


class Email():
    def __init__(self,token=""):
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

        self._query_formulas = [
            "false",  # rejects everything
            "true",  # accepts everything
            "m",  # email starts with numeric symbols
            "!(F(a))",  # there is no '@'
            "!(F(d))",  # there is no '.'
            "!(F(p))",
            "!(F(m))",
            "F(&(a,X(F(a))))",
            "F(&(d,X(F(d))))",
            "F(&(d,X(F(m))))",
            "F(&(d,X(G(p))))",
            "F(&(a,X(G(!(d)))))",
            "&(&(&(!(F(m)),F(U(p,a))),F(&(a,X(U(p,d))))),F(&(d,X(G(p)))))",
            "F(&(a,X(d)))",
            "G(m)",  
            "!(p)",
            "a", 
            "d", 
            "&(&(F(U(|(p,m),a)),F(&(a,X(U(|(p,m),d))))),F(&(d,X(G(p)))))",
            "F(&(a,X(d)))",
            
        ]

        dic = {
            "a" : "x0",
            "d" : "x1",
            "m" : "x2",
            "p" : "x3"
        }
        
        self.query_formulas = []
        for formula in self._query_formulas:
            if(formula != "false" and formula != "true"):
                for key in dic:
                    formula = formula.replace(key, dic[key])
            self.query_formulas.append(formula)

        # self.query_formulas = self.query_formulas[18:]
        # print(self.query_formulas)


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

    def __init__(self, token=""):
        self._bp_other_letters = "a"
        self.alphabet = "lr" + self._bp_other_letters
        self.target_formula = "balanced parentheses"

        self._query_formulas = [
            "false",  
            "true",
            "!(F(|(l,r)))", 
            "G(->(l,F(r)))",
            "G(->(l,!(F(r))))",
            "G(->(l,F(|(a,r))))",
            "G(->(l,!(F(|(a,r)))))",
            "G(a)",
            "r",  # starts with right parenthesis
            "U(a,r)", 
            "F(&(l,X(G(!(r)))))",
            "G(l)",
            "&(&(F(l),F(r)),F(U(|(l,a),r)))",
            "&(&(F(l),F(r)),!(F(U(|(l,a),r))))",
        ]


        dic = {
            "l" : "x0",
            "r" : "x1",
            "a" : "x2"
        }
        
        self.query_formulas = []
        for formula in self._query_formulas:
            if(formula != "false" and formula != "true"):
                for key in dic:
                    formula = formula.replace(key, dic[key])
            self.query_formulas.append(formula)

        self.query_formulas = self.query_formulas[12:]
        # print(self.query_formulas)

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
    def __init__(self, token="", max_words = 1000, max_len = 150):
        self.target_formula = "Text classification"
        self.alphabet = ["x" + str(i) for i in range(max_words + 1)]
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
        self.tok = Tokenizer(num_words=self._max_words)
        self.tok.fit_on_texts(df['text'])
        sequences = self.tok.texts_to_sequences(df['text'])
        sequences_matrix = sequence.pad_sequences(sequences,maxlen=self._max_len)
        # print(sequences_matrix, Y)
        self.dict = {}
        for A, B in zip(sequences_matrix, Y):
            # print(tuple(A),B[0] == 1)
            self.dict[("").join(["x"+str(c) for c in A])] = B[0] == 1

    def classify_word(self, w):
        if(w not in self.dict):
            print(w)
            raise ValueError("word not in the original file")
        else:
            return self.dict[w]

class Deceptive_Opinion():
    def __init__(self, max_words = 1000, max_len = 500):
        self.target_formula = "Deceptive opinion"
        self.alphabet = ["x" + str(i) for i in range(max_words + 1)]
        self.query_formulas = [
        ]
        self._max_words = max_words
        self._max_len = max_len


        df = pd.read_csv('benchmarks/raw/deceptive-opinion.csv',delimiter=',',encoding='latin-1')
        df = df[df['polarity'] == 'positive']
        df = df[['deceptive', 'text']]
        le = LabelEncoder()
        Y = le.fit_transform(df['deceptive'])
        Y = Y.reshape(-1,1)
        
        # tokenize
        self.tok = Tokenizer(num_words=self._max_words)
        self.tok.fit_on_texts(df['text'])
        sequences = self.tok.texts_to_sequences(df['text'])
        sequences_matrix = sequence.pad_sequences(sequences,maxlen=self._max_len)
        # print(sequences_matrix, Y)
        self.dict = {}
        for A, B in zip(sequences_matrix, Y):
            # print(tuple(A), B[0] == 1)
            self.dict[("").join(["x"+str(c) for c in A])] = B[0] == 1
        

    def classify_word(self, w):
        if(w not in self.dict):
            print(w)
            raise ValueError("word not in the original file")
        else:
            return self.dict[w]

from samples2ltl.utils.SimpleTree import Formula        
from samples2ltl.utils.Traces import Trace


class Example:
    def __init__(self, alphabet, target_formula, token):
        self.alphabet = alphabet
        self.target_formula = target_formula
        # self.dfa = ltlf2dfa.translate_ltl2dfa(
        #     alphabet=[character for character in self.alphabet], formula=self.target_formula, token=str(token))
        # self.classify_word = self.dfa.classify_word
        self.ltl_formula = Formula.convertTextToFormula(self.target_formula)        
        

    def classify_word(self, w):
        w = w.split("x")[1:]
        trace_vector = []
        for letter in w:
            trace_vector.append([self.alphabet[i][1:] == letter for i in range(len(self.alphabet))])
        if(len(w) == 0):
            trace = Trace([[False for _ in self.alphabet]])
        else:
            trace = Trace(trace_vector)
        return trace.evaluateFormulaOnTrace(self.ltl_formula)


class Example1(Example):

    def __init__(self, token=""):
        # super().__init__(alphabet="abc", target_formula="G(~a)", token=token)
        super().__init__(alphabet=['x0', 'x1', 'x2'], target_formula="G(!(x0))", token=token)
    
        self.query_formulas = [
            "true",
            "false",
            "x0",
            "!(x0)",
            'F(x0)',
            "F(!(x0))",
            "F(x1)",
            "F(|(x1,x2))",
            "G(|(x1,x2))",
            'X(G(!(x0)))',
            'X(G(x0))'
        ]


class Example2(Example):

    def __init__(self, token=""):
        # super().__init__(alphabet="abc", target_formula="G(a->X(b))", token=token)
        super().__init__(alphabet=['x0', 'x1', 'x2'], target_formula="G(->(x0,X(x1)))", token=token)
    
        self.query_formulas = [
            "true",
            "false",
            "x1",
            "X(x1)",
            "G(x1)",
            "F(x0)",
            "G(x0)",
        ]


class Example3(Example):

    def __init__(self, token=""):
        super().__init__(alphabet=['x0', 'x1', 'x2'], target_formula="G(&(->(x0,X(x1)),->(X(x1),x0)))", token=token)
    
        self.query_formulas = [
            "true",
            "false",
            'G(x1)',
            'G(!(x0))',
            'G(x0)',
            'F(x2)'
        ]




class Example4(Example):

    def __init__(self, token=""):
        super().__init__(alphabet=['x0', 'x1', 'x2'], target_formula="F(x0)", token=token)
    
        self.query_formulas = [
            "true",
            "false",
            "F(x1)",
            "F(!(x0))",
            "F(!(x1))",
            'F(U(x0,x1))',
            'F(U(x1,x0))',
            "G(x0)",
            "G(x2)",
            "F(x2)",
            "F(&(x0,X(x1)))"
        ]
    
    

class Example5(Example):

    def __init__(self, token=""):
        super().__init__(alphabet=['x0', 'x1', 'x2'], target_formula="F(U(x0,x1))", token=token)

        self.query_formulas = [
            "true",
            "false",
            "F(x0)",
            "F(U(x0,x1))",
            "F(U(x1,x0))",
            "G(x0)",
            "G(x2)",
            "F(x2)",
            "F(&(x0,X(x1)))"
        ]


class Example6(Example):

    def __init__(self, token=""):
        # super().__init__(alphabet="abc", target_formula="F(a & X(b))", token=token)
        super().__init__(alphabet=['x0', 'x1', 'x2'], target_formula="F(&(x0,X(x1)))", token=token)
        
        self.query_formulas = [
            "true",
            "false",
            "F(x0)",
            "F(x1)",
            "F(x2)",
            "G(x0)",
            "F(U(x0,x1))"
        ]


class Example7(Example):

    def __init__(self, token=""):
        # super().__init__(alphabet="abc", target_formula="G(a)", token=token)
        super().__init__(alphabet=['x0', 'x1', 'x2'], target_formula="G(x0)", token=token)
    
        self.query_formulas = [
            "true",
            "false",
            "F(x0)",
            "F(x1)",
            "F(|(x0,x1))",
            "F(U(x0,x1))"
        ]




'''
['F(x2)', 'F(x2)', 'F(|(x33,x73))', '|(x244,F(x47))', '|(x114,F(x341))', '|(x106,F(x2))', 'X(|(x13,x22))', '|(x591,F(x5))', '|(x235,F(x48))', '|(x104,F(x337))', '|(x106,F(x22))', '|(x528,F(x169))', '|(x6,F(x15))', '|(x127,F(x620))', '|(x179,F(x42))', 'U(!(x1),x2)', 'F(x4)', '|(x488,F(x9))', 'F(x42)', '|(x47,x720)', 'F(|(x48,x960))', '|(x637,F(x47))', 'F(x2)', '|(x773,F(x26))', '|(x13,F(x96))', '|(x48,F(x13))', 'F(x26)', '|(x12,F(x16))', '|(x298,|(x210,x3))', 'F(x2)', '|(x7,|(x244,x3))', 'F(|(x106,x21))', '|(x324,|(x2,x420))', 'F(x16)', '|(x100,F(x3))', 'F(|(x16,x227))', 'F(|(x48,x73))', 'F(|(x124,x210))', 'F(x47)', '|(x12,F(x18))', 'F(|(x230,x3))', 'F(x26)', '|(x289,F(x16))', '|(x257,x53)', 'F(x6)', 'F(x5)', 'F(x388)', 'F(x912)', 'F(x8)', '|(x192,x7)', 'F(x16)', '|(x344,x47)', '|(x21,x39)', 'F(x2)', '|(x222,x39)', '|(x113,x3)', '|(x113,x178)', 'F(x4)', 'F(x7)', 'F(x68)', '|(x1,x94)', 'F(x2)', 'F(x197)', '|(x178,x3)', 'F(x38)', 'F(x47)', 'F(x16)', '|(x28,x438)', 'F(x31)', 'F(|(x15,x21))', 'F(x16)', '|(x113,F(x19))', '|(x12,F(x42))', 'F(x21)', '|(x100,F(x4))', '|(x13,F(x9))', 'F(x96)', 'F(x2)', 'U(!(x118),x4)', '|(x378,F(x2))', 'F(x2)', '|(x40,F(x35))', '|(x12,F(x591))', '|(x47,x736)', 'F(x2)', '|(x222,F(x31))', 'F(|(x12,x21))', '|(x178,F(x2))', 'F(x16)', 'F(x2)', '|(x797,F(x13))', 'F(x19)', 'F(x13)', 'F(|(x368,x84))', '|(x121,F(x5))', '|(x16,F(x4))', 'F(|(x416,x84))', 'F(|(x124,x252))', 'F(x84)', 'F(x42)', '|(x175,F(x3))', '|(x703,F(x42))', '|(x136,x48)', 'G(!(x1))', '|(x242,F(x5))', '|(x848,X(x13))', '|(x483,F(x13))', '|(x172,F(x2))', 'F(x12)', '|(x719,F(x501))', 'F(|(x17,x242))', '->(F(x9),x40)', 'F(x12)', '|(x73,F(x7))', 'F(x2)', '|(x342,F(x101))', 'F(x4)', '|(x192,F(x101))', '|(x192,F(x19))', '|(x341,|(x49,x797))', 'F(x2)', 'U(!(x3),x2)', '|(x263,F(x47))', '|(x83,F(x873))', 'F(|(x323,x4))', 'F(x2)', '|(x47,F(x26))', 'F(x2)', 'F(x12)', '|(x482,F(x124))', '|(x35,F(x16))', 'F(x16)', '|(x12,F(x2))', 'F(x13)', '|(x27,F(x119))', 'F(|(x147,x47))', '|(x62,F(x2))', '|(x148,F(x21))', 'F(x4)', 'F(|(x122,x31))', 'U(!(x53),x2)', 'F(x2)', '|(x1,F(x16))', '|(x235,F(x650))', 'F(|(x73,x86))', '|(x175,F(x19))', 'F(|(x113,x6))', '|(x124,F(x19))', 'F(|(x13,x295))', '|(x47,x773)', '|(x123,|(x4,x538))', 'F(x124)', 'F(x92)', 'F(x16)', '!(F(x1))', '|(x3,F(x39))', 'F(|(x124,x696))', '|(x3,F(x21))', 'F(|(x105,x47))', 'F(x4)', '|(x797,F(x26))', '|(x113,F(x16))', '|(x172,|(x495,x504))', 'F(|(x148,x71))', '|(x495,F(x96))', '|(x3,F(x141))', '|(x188,F(x21))', '|(x27,x35)', 'F(x3)', 'F(x36)', '|(x70,F(x96))', '|(x226,F(x96))', 'F(x2)', 'U(!(x495),x2)', 'F(x2)', 'F(x16)', '|(x47,F(x2))', 'F(x2)', 'F(x13)', 'F(x13)', '|(x641,F(x2))', '|(x22,F(x12))', 'F(|(x2,x958))', 'F(x2)', '|(x113,F(x3))', '|(x889,F(x35))', 'F(x2)', '|(x40,F(x19))', '|(x756,F(x12))', 'F(x13)', 'F(x73)', 'F(x16)', '|(x192,x483)', 'F(|(x40,x84))', 'F(x2)', 'F(x16)', '|(x323,F(x16))', '|(x192,x583)', '|(x70,F(x12))', 'F(|(x16,x462))']
'''