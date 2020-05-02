# from PACTeacher.dfa import DFA
from PACTeacher.random_words import random_word_by_letter, bfs_random
# from PACTeacher.teacher import Teacher
import numpy as np
import math
import time
import signal
from contextlib import contextmanager
from multiprocessing import Process, Queue

# @contextmanager
# def timeout(time):
#     # Register a function to raise a TimeoutError on the signal.
#     signal.signal(signal.SIGALRM, raise_timeout)
#     # Schedule the signal to be sent after ``time``.
#     signal.alarm(time)

#     try:
#         yield
#     except TimeoutError:
#         pass
#     finally:
#         # Unregister the signal so it won't be triggered
#         # if the timeout is not reached.
#         signal.signal(signal.SIGALRM, signal.SIG_IGN)


# def raise_timeout(signum, frame):
#     raise TimeoutError



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
        self._last_counterexample_positive=False

    def equivalence_query_dfs(self, dfa, verbose=False):
        self._num_equivalence_asked = self._num_equivalence_asked + 1

        if(self.query_dfa is None):
            if dfa.is_word_in("") != self.specification_dfa.is_word_in(""):
                return ""
        else:
            if dfa.is_word_in("") != (self.query_dfa.is_word_in("") and self.specification_dfa.is_word_in("")):
                return ""

        positive_counterexamples=[]
        negative_counterexamples=[]
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
                        """  
                        The following code tries to balance between positive and negative counterexamples.
                        """
                        if(not dfa_verdict): # if current verdict is negative, the word must be a positive counterexample
                            positive_counterexamples.append(word)
                        else:
                            negative_counterexamples.append(word)
                        
                        break
                        # return word
                    
                    
                # impose bound on word-length
                word_length+=1
                if(self.max_trace_length <= word_length):
                    break
            
        """ 
        try to return the minimal-size counterexample with alteration
        """
        negative_counterexamples = sorted(negative_counterexamples, key=lambda x:len(x))
        positive_counterexamples = sorted(positive_counterexamples, key=lambda x:len(x))

        
        if(self._last_counterexample_positive):
            

            if(len(negative_counterexamples)!=0):
                self._last_counterexample_positive = False
                return negative_counterexamples[0]
            elif(len(positive_counterexamples)!=0):
                if(verbose):
                    print("No negative counterexample found")
                return positive_counterexamples[0]
        else:
            
            if(len(positive_counterexamples)!=0):
                self._last_counterexample_positive = True
                return positive_counterexamples[0]
            elif(len(negative_counterexamples)!=0):
                if(verbose):
                    print("No positive counterexample found")
                return negative_counterexamples[0]
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

    def teach(self, learner, traces, timeout = 20, verbose=True):
        # with timeout(time):

            start_time=time.time()

            for i in range(100):

                
                if(learner.current_formula_depth>self.max_formula_depth):
                    if(verbose):
                        print("Max formula depth achieved")
                    return learner, False
                """  
                For LTL learning, initialize  a process
                """
                q = Queue()
                p = Process(target = learner.learn_ltlf_and_dfa, args = (q,))
                p.start()
                p.join(timeout=max(0.5, timeout-(time.time()-start_time)))
                p.terminate()
                while p.exitcode == None:
                    time.sleep(1)
                if p.exitcode == 0:
                    
                    [learner] = q.get()
                
                    # learner.learn_ltlf_and_dfa()
                    counterexample = self.equivalence_query_dfs(learner.dfa, verbose=verbose)
                    if counterexample is None:
                        return learner,  True

                    if(self.query_dfa is None):
                        if(self.specification_dfa.classify_word(counterexample)):
                            if(verbose):
            
                                print("new counterexample:", counterexample, " should be accepted by implementation")
                            traces.add_positive_example(counterexample)
                        else:
                            if(verbose):
            
                                print("new counterexample:", counterexample, " should be rejected by implementation")
                            traces.add_negative_example(counterexample)
                    else:
                        if(self.specification_dfa.classify_word(counterexample) and self.query_dfa.classify_word(counterexample)):
                            if(verbose):
            
                                print("new counterexample:", counterexample, " should be accepted by implementation")
                            traces.add_positive_example(counterexample)
                        else:
                            if(verbose):
            
                                print("new counterexample:", counterexample, " should be rejected by implementation")
                            traces.add_negative_example(counterexample)
                else:
                    return learner, False            


                print(i," iteration complete\n\n\n")
                
            
            return learner, False

            

            # break


    # n > (log(delta) -num_round) / log(1-epsilon)
