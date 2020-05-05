import random
import exrex
import rstr
import re
import LTL2DFA as ltlf2dfa


# construct a dfa that implements alternating bit protocol
class Alternating_Bit_Protocol:
    def __init__(self):
        self.dfa = ltlf2dfa.DFA()
        self.target_formula = "alternating bit protocol"
        self.construct_dfa()

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
        for length in range(4,max_length+1):
            for i in range(int(n/(max_length-3))):
                prefix_length = random.randint(0, length-4)  # the part before '@'
                suffix_length = length-prefix_length-3
                r = "("+self._letter_symbols_regex + \
                    "){1}" + "("+self._all_symbols_regex+")" + \
                    "{" + str(prefix_length) + "}" + self._at_the_rate + "(" + self._letter_symbols_regex +\
                    "){" + str(suffix_length) + "}"+self._dot
                strings.append(exrex.getone(r))
                assert(self.classify_word(strings[-1])), strings[-1]+" classification error"
        return strings


