# from PACTeacher.dfa import DFA
from PACTeacher.random_words import random_word_by_letter
# from PACTeacher.teacher import Teacher
import numpy as np
import math

class PACTeacher():

    def __init__(self, dfa, epsilon=0.05, delta=0.05, max_trace_length=20, max_formula_depth=20, query_dfa=None):
        assert((epsilon <= 1) & (delta <= 1))
        # Teacher.__init__(self, specification_dfa)
        self.specification_dfa=dfa
        self.epsilon = epsilon
        self.query_dfa=query_dfa
        self.delta = delta
        self._log_delta = np.log(delta)
        self._log_one_minus_epsilon = np.log(1-epsilon)
        self._num_equivalence_asked = 0
        self.max_trace_length=max_trace_length
        self.max_formula_depth=max_formula_depth

    def equivalence_query(self, dfa):
        self._num_equivalence_asked = self._num_equivalence_asked + 1

        # initial check
        if dfa.is_word_in("") != self.specification_dfa.is_word_in(""):
            return ""

        
        # number_of_rounds = int((self._log_delta - self._num_equivalence_asked)/self._log_one_minus_epsilon)
        number_of_rounds = int(math.ceil((self._num_equivalence_asked*0.693147-self._log_delta)/self.epsilon))
        
        # do conformance testing on query first
        if(self.query_dfa is not None):
        
            for i in range(number_of_rounds):
            
                dfa.reset_current_to_init()
                self.query_dfa.reset_current_to_init()
                word = ""
                word_length=0
                for letter in random_word_by_letter(self.specification_dfa.alphabet):
                    word = word + letter
                    if dfa.is_word_letter_by_letter(letter) != self.query_dfa.is_word_letter_by_letter(letter):
                        return word
                    # impose bound on word-length
                    word_length+=1
                    if(self.max_trace_length <= word_length):
                        break



        for i in range(number_of_rounds):

            dfa.reset_current_to_init()
            self.specification_dfa.reset_current_to_init()
            word = ""
            word_length=0
            for letter in random_word_by_letter(self.specification_dfa.alphabet):
                word = word + letter

                if(self.query_dfa is not None):
                    # check with network
                    if dfa.is_word_letter_by_letter(letter) != self.specification_dfa.is_word_letter_by_letter(letter):
                        return word
                else:
                    # If the code reaches here then L(LTL) \subset L(query). 
                    # Now do conformance testing of query on network

                    if self.query_dfa.is_word_letter_by_letter(letter) != self.specification_dfa.is_word_letter_by_letter(letter):
                        return word

                # impose bound on word-length
                word_length+=1
                if(self.max_trace_length <= word_length):
                    break

        return None

    def membership_query(self, w):
        return self.specification_dfa.is_word_in(w)

    def teach(self, learner, traces):
        # we really do not need to pass the teacher in the following line. 
        # learner.teacher = self


        for i in range(100):
            if(learner.current_formula_depth>self.max_formula_depth):
                print("Max formula depth achieved")
                break
            
            learner.learn_ltlf_and_dfa()
            counterexample = self.equivalence_query(learner.dfa)
            if counterexample is None:
                break
            # learner.new_counterexample(counter)
            if(self.specification_dfa.classify_word(counterexample)):
                print("new counterexample:", counterexample, " should be accepted by implementation")
                traces.add_positive_example(counterexample)
            else:
                print("new counterexample:", counterexample, " should be rejected by implementation")
                traces.add_negative_example(counterexample)
            print("\n\n\n")
            

            # break


    # n > (log(delta) -num_round) / log(1-epsilon)
