import numpy as np
import random
import exrex
import rstr
import re
import LTL2DFA as ltlf2dfa
import random
import string
from RNN2DFA.Training_Functions import make_train_set_for_target


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
            "F(a&X(c))",  # eventually bit 0 is followed by ack 0
            # eventually bit 0 is followed by ack 0 and eventually bit 1 is followed by ack 1
            "(F(a&X(c))) | (F(b&X(d)))",
            "F(a&X(b))",  # Eventually bit 0 is followed by bit 1 (should be false)
            "F(b&X(a))",  # vice versa
            "F(c&X(d))",  # eventually ack 0 is followed by ack 1
            "F(d&X(c))",  # vice versa
            "~F(a & X(a))",  # reduce space: consecutive bit 0 is not transmitted
            "~F(b & X(b))",  # reduce space: consecutive bit 1 is not transmitted
            "~F(c & X(c))",  # reduce space: consecutive ack 0 is not transmitted
            "~F(d & X(d))",  # reduce space: consecutive ack 1 is not transmitted
            # it is not the case that eventually ack 0 is transmitted until bit 0 is transmitted
            "~F( a U c )",
            # it is not the case that eventually ack 1 is transmitted until bit 1 is transmitted
            "~F( b U d )",
            # if both bit 0 and bit 1 is present, then there must be ack 0
            "(F(a) & F(b)) -> F(c) "

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
        self.dfa.F = [0, 2]
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


class Email():
    def __init__(self):
        self._at_the_rate = "a"
        self._dot = "d"
        self._numerical_symbols = "mn"
        self._letter_symbols = "pqr"
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
            "(m|n)",  # email starts with numeric symbols
            "~F(a)",  # there is no '@'
            "~F(d)",  # there is no '.'
            "F(a & X(m|n))",  # @ is followed by numerical symbols
            "F((m|n) & X(d))",  # numerical symbols are followed by '.'
            "G(m|n)",  # only numeric
            # if there is a numeric symbol, then letters are true until the numeric symbol appears
            "F(m|n)->((p|q|r)U(m|n))",
            "~(F(m|n)->((p|q|r)U(m|n)))",  # opposite to the earlier query
            # there is a numeric symbol and it must satisfy the constraint that letters are true until
            "(F(m|n))&((p|q|r)U(m|n))",
            # numeric symbols are true
            "(F(m|n))&(F(a & X(m|n)))"

        ]

    def _construct_regex(self):
        before_at_the_rate_only_letter = "("+"|".join(
            char for char in self._letter_symbols)+")"
        before_at_the_rate_both = "("+"|".join(
            char for char in self._letter_symbols+self._numerical_symbols)+")"

        self.regex = before_at_the_rate_only_letter + \
            before_at_the_rate_both + \
            "*" + \
            self._at_the_rate + \
            before_at_the_rate_only_letter + \
            "+" + \
            self._dot + \
            "$"
        # print(self.regex)

    def classify_word(self, word):
        return bool(re.match(self.regex, word))
        pass

    def generate_matching_strings(self, n, max_length=20):
        strings = []
        for length in range(4, max_length+1):
            for i in range(int(n/(max_length-3))):
                prefix_length = random.randint(
                    0, length-4)  # the part before '@'
                suffix_length = length-prefix_length-3
                r = "("+self._letter_symbols_regex + \
                    "){1}" + "("+self._all_symbols_regex+")" + \
                    "{" + str(prefix_length) + "}" + self._at_the_rate + "(" + self._letter_symbols_regex +\
                    "){" + str(suffix_length) + "}"+self._dot
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
        self._bp_other_letters = "abcd"
        self.alphabet = "lr" + self._bp_other_letters
        self.target_formula = "balanced parentheses"

        self.query_formulas = [
            "false",  # rejects everything
            "~F(l|r)",  # no parenthesis (both left and right)
            "F(l&X(~l))",  # no consecutive left parentheses
            # globally it is true that if there is a left parenthesis, then there is a
            "G(l->(l & X(r)))",
            # right parenthesis next to it
            "true",  # accepts everything
            "(F(l) & F(r))",  # eventually l is true and r is true
            "F(l U (~l))",  # eventually l is true until ~l is true
            "G(~l)"  # globally ~l is true
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
        super().__init__(alphabet="abc", target_formula="G(b->X(~a))", token=token)

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
        super().__init__(alphabet="abc", target_formula="F(a)", token=token)

        self.query_formulas = [
            "true",
            "false",
            "F(b)",
            "F(~a)",
            "F(~b)",
            'F(aUb)',
            'F(bUa)' 
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
        super().__init__(alphabet="abc", target_formula="G(b -> G(a))", token=token)

        self.query_formulas = [
            "true",
            "false",
        ]
