import time
import timeit
import unittest

from PACTeacher.dfa import DFA, random_dfa
from PACTeacher.exact_teacher import ExactTeacher
from PACTeacher.learner_decison_tree import DecisionTreeLearner
from PACTeacher.pac_teacher import PACTeacher


class Test(unittest.TestCase):

    def test_dfa(self):
        # dfa with the language a*b*
        dfa = DFA(1, {1, 2}, {1: {"a": 1, "b": 2},
                              2: {"a": 3, "b": 2},
                              3: {"a": 3, "b": 3}})
        self.assertTrue(dfa.is_word_in(""))
        self.assertTrue(dfa.is_word_in("aaaabbb"))
        self.assertFalse(dfa.is_word_in("aaabaaaabbbbbb"))

        # dfa with the language immediately after every "a" there is a "b"
        dfa = DFA(1, {1}, {1: {"a": 2, "b": 1, "c": 1},
                           2: {"a": 3, "b": 1, "c": 3},
                           3: {"a": 3, "b": 3, "c": 3}})
        self.assertTrue(dfa.is_word_in("abccccbbbbcccabababccccc"))
        self.assertFalse(dfa.is_word_in("abccccbbabbcccaabababaaaa"))

        dfa2 = DFA(1, {1, 4}, {1: {"a": 2, "b": 1, "c": 1},
                               2: {"a": 3, "b": 1, "c": 3},
                               3: {"a": 3, "b": 3, "c": 4},
                               4: {"a": 3, "b": 3, "c": 4}})

        # dfa with the language immediately after every "a" there is a "b"
        dfa3 = DFA(1, {1, 5}, {1: {"a": 2, "b": 5, "c": 5},
                               2: {"a": 3, "b": 1, "c": 3},
                               3: {"a": 4, "b": 4, "c": 4},
                               4: {"a": 3, "b": 3, "c": 3},
                               5: {"a": 2, "b": 1, "c": 1}})

        self.assertTrue(dfa == dfa)
        self.assertTrue(dfa == dfa3)
        self.assertTrue(dfa != dfa2)

    def test_learning_algo(self):
        dfa = DFA(1, {1}, {1: {"a": 2, "b": 1, "c": 1},
                           2: {"a": 3, "b": 1, "c": 3},
                           3: {"a": 3, "b": 3, "c": 3}})

        # dfa with the language immediately after every "a" there is a "b"
        dfa2 = DFA(1, {1, 5}, {1: {"a": 2, "b": 5, "c": 5},
                               2: {"a": 3, "b": 1, "c": 3},
                               3: {"a": 4, "b": 4, "c": 4},
                               4: {"a": 3, "b": 3, "c": 3},
                               5: {"a": 2, "b": 1, "c": 1}})

        teacher_exact = ExactTeacher(dfa2)
        student_exact = DecisionTreeLearner(teacher_exact)
        teacher_exact.teach(student_exact)
        self.assertTrue(dfa == student_exact.dfa)

        for i in range(2):
            dfa_rand = random_dfa(["a", "b", "c", "d", "e"], min_states=500, max_states=501, min_final=1,
                                  max_final=10)
            teacher_exact = ExactTeacher(dfa_rand)
            student_exact = DecisionTreeLearner(teacher_exact)

            init_time = time.time()
            teacher_exact.teach(student_exact)
            print("exact: " + str(time.time() - init_time))
            self.assertTrue(dfa_rand == student_exact.dfa)

            teacher_pac = PACTeacher(dfa_rand)
            student_pac = DecisionTreeLearner(teacher_pac)

            count = -1
            init_time = time.time()
            while dfa_rand != student_pac.dfa:
                count = count + 1
                teacher_pac.teach(student_pac)
            print("PAC: " + str(time.time() - init_time) + ", restarted learning process " + str(count) + " times.")
