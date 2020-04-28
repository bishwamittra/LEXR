# from PACTeacher.dfa import DFA
from PACTeacher.random_words import random_word_by_letter, bfs_random
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

    def equivalence_query_dfs(self, dfa):
        self._num_equivalence_asked = self._num_equivalence_asked + 1

        if(self.query_dfa is None):
            if dfa.is_word_in("") != self.specification_dfa.is_word_in(""):
                return ""
        else:
            if dfa.is_word_in("") != (self.query_dfa.is_word_in("") and self.specification_dfa.is_word_in("")):
                return ""

        # number_of_rounds = int((self._log_delta - self._num_equivalence_asked)/self._log_one_minus_epsilon)

        # from the paper
        number_of_rounds = int(math.ceil((self._num_equivalence_asked*0.693147-self._log_delta)/self.epsilon))
        for i in range(number_of_rounds):
            dfa.reset_current_to_init()
            self.specification_dfa.reset_current_to_init()
            if(self.query_dfa is not None):
                self.query_dfa.reset_current_to_init()
            word = ""
            word_length=0
            for letter in random_word_by_letter(self.specification_dfa.alphabet):
                word = word + letter
                """ 
                the following code fragment narrow downs the search space with the help of query dfa. 
                """
                if(self.query_dfa == None):
                    if dfa.is_word_letter_by_letter(letter) != self.specification_dfa.is_word_letter_by_letter(letter):
                        return word
                else:
                    dfa_verdict= dfa.is_word_letter_by_letter(letter)
                    specification_verdict=self.specification_dfa.is_word_letter_by_letter(letter)
                    query_verdict=self.query_dfa.is_word_letter_by_letter(letter)

                    if(dfa_verdict != (specification_verdict and query_verdict)):
                        return word
                    
                    
                # impose bound on word-length
                word_length+=1
                if(self.max_trace_length <= word_length):
                    break

        return None
        
    """  
    A BFS traversal on randomly generated words
    """    
    def equivalence_query_bfs(self, dfa):
        self._num_equivalence_asked = self._num_equivalence_asked + 1

        if(self.query_dfa is None):
            if dfa.is_word_in("") != self.specification_dfa.is_word_in(""):
                return ""
        else:
            if dfa.is_word_in("") != (self.query_dfa.is_word_in("") and self.specification_dfa.is_word_in("")):
                return ""

        # number_of_rounds = int((self._log_delta - self._num_equivalence_asked)/self._log_one_minus_epsilon)

        # from the paper
        number_of_rounds = int(math.ceil((self._num_equivalence_asked*0.693147-self._log_delta)/self.epsilon))

        words=["" for i in range(number_of_rounds)] 
        dfa_state=[dfa.reset_current_to_init() for i in range(number_of_rounds)]
        specification_state=[self.specification_dfa.reset_current_to_init() for i in range(number_of_rounds)]

        if(self.query_dfa is not None):
            query_state=[self.query_dfa.reset_current_to_init() for i in range(number_of_rounds)]

        for _ in range(self.max_trace_length):
            index=0
            for letter in bfs_random(self.specification_dfa.alphabet,number_of_rounds):
                words[index]+=letter

                """  
                specify automata states during traversal
                """
                dfa.current_state=dfa_state[index]
                self.specification_dfa.current_state=specification_state[index]
                
                
                # get verdict from DFAs
                dfa_verdict= dfa.is_word_letter_by_letter(letter)
                specification_verdict=self.specification_dfa.is_word_letter_by_letter(letter)

                # remember automata state after traversal
                dfa_state[index]=dfa.current_state
                specification_state[index]=self.specification_dfa.current_state
                
                # repeat everything when query is specified
                if(self.query_dfa is not None):
                    self.query_dfa.current_state=query_state[index]
                    query_verdict=self.query_dfa.is_word_letter_by_letter(letter)
                    query_state[index]=self.query_dfa.current_state
        


                if(self.query_dfa == None):
                    if dfa_verdict != specification_verdict:
                        return words[index]
                else:

                    if(dfa_verdict != (specification_verdict and query_verdict)):
                        return words[index]
                    

                index+=1
                pass

        

        return None
    

    def membership_query(self, w):
        return self.specification_dfa.is_word_in(w)

    def teach(self, learner, traces):
        # we really do not need to pass the teacher in the following line. 
        # learner.teacher = self


        for i in range(10):

            # print(i)
            if(learner.current_formula_depth>self.max_formula_depth):
                print("Max formula depth achieved")
                break
            
            learner.learn_ltlf_and_dfa()
            counterexample = self.equivalence_query_dfs(learner.dfa)
            if counterexample is None:
                return True
                break
            # learner.new_counterexample(counter)

            if(self.query_dfa is None):
                if(self.specification_dfa.classify_word(counterexample)):
                    print("new counterexample:", counterexample, " should be accepted by implementation")
                    traces.add_positive_example(counterexample)
                else:
                    print("new counterexample:", counterexample, " should be rejected by implementation")
                    traces.add_negative_example(counterexample)
            else:
                if(self.specification_dfa.classify_word(counterexample) and self.query_dfa.classify_word(counterexample)):
                    print("new counterexample:", counterexample, " should be accepted by implementation")
                    traces.add_positive_example(counterexample)
                else:
                    print("new counterexample:", counterexample, " should be rejected by implementation")
                    traces.add_negative_example(counterexample)

            print("\n\n\n")

        return False
            

            # break


    # n > (log(delta) -num_round) / log(1-epsilon)
