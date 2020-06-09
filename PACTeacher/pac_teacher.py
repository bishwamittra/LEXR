# from PACTeacher.dfa import DFA
from PACTeacher.random_words import random_word_by_letter, bfs_random
# from PACTeacher.teacher import Teacher
import numpy as np
import math
import time
import signal
from contextlib import contextmanager
from multiprocessing import Process, Queue
import operator as op
from functools import reduce

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
        self.specification_dfa = dfa
        self.epsilon = epsilon
        self.query_dfa = query_dfa
        self.delta = delta
        self._log_delta = np.log(delta)
        self._log_one_minus_epsilon = np.log(1-epsilon)
        self._num_equivalence_asked = 0
        self.max_trace_length = max_trace_length
        self.max_formula_depth = max_formula_depth
        self._last_counterexample_positive = False
        self.returned_counterexamples = []
        self._num_counterexamples_in_EQ = None
        self._number_of_samples = None
        self.number_of_words_checked = 0

    def equivalence_query(self, dfa, verbose=False):

        # if(verbose):
        #     print("already found counterexamples:", self.returned_counterexamples)

        _max_trace_length = self.max_trace_length

        self._num_counterexamples_in_EQ = 0

        self._num_equivalence_asked = self._num_equivalence_asked + 1

        if(self.query_dfa is None):
            self.number_of_words_checked += 1
            if dfa.is_word_in("") != self.specification_dfa.is_word_in(""):
                return ""
        else:
            self.number_of_words_checked += 1
            if (dfa.is_word_in("") != (self.query_dfa.is_word_in("") and self.specification_dfa.is_word_in(""))) and "" not in self.returned_counterexamples:
                return ""

        positive_counterexample = None
        negative_counterexample = None
        # number_of_rounds = int((self._log_delta - self._num_equivalence_asked)/self._log_one_minus_epsilon)

        # from the paper
        self._number_of_samples = int(
            math.ceil((self._num_equivalence_asked*0.693147-self._log_delta)/self.epsilon))
        for i in range(self._number_of_samples):

            self.number_of_words_checked += 1


            """  
            # when both positive and negative counterexamples are found, one can safely decrease the max_trace_length for the current 
            # equivalence query
            """

            if(negative_counterexample is not None and positive_counterexample is not None):
                # if(verbose):
                #     print("decreasing maximum trace length to ", _max_trace_length)
                if(self._last_counterexample_positive):
                    _max_trace_length = len(negative_counterexample) - 1
                else:
                    _max_trace_length = len(positive_counterexample) - 1

            dfa.reset_current_to_init()
            # renew rnn (applicable for dynet package)
            self.specification_dfa.renew()
            self.specification_dfa.reset_current_to_init()

            if(self.query_dfa is not None):
                self.query_dfa.reset_current_to_init()
            word = ""
            word_length = 0
            for letter in random_word_by_letter(self.specification_dfa.alphabet):
                word = word + letter
                word_length += 1

                """ 
                the following code fragment narrow downs the search space with the help of query dfa. 
                """
                if(self.query_dfa == None):
                    if dfa.is_word_letter_by_letter(letter) != self.specification_dfa.is_word_letter_by_letter(letter):
                        return word
                else:

                    dfa_verdict = dfa.is_word_letter_by_letter(letter)
                    specification_verdict = self.specification_dfa.is_word_letter_by_letter(
                        letter)
                    query_verdict = self.query_dfa.is_word_letter_by_letter(
                        letter)

                    if(dfa_verdict != (specification_verdict and query_verdict)):
                        """  
                        The following code tries to balance between positive and negative counterexamples.
                        """
                        if(not dfa_verdict):  # if current verdict is negative, the word must be a positive counterexample
                            if((positive_counterexample is None or len(positive_counterexample) > word_length) and word not in self.returned_counterexamples):
                                positive_counterexample = word
                        else:
                            if((negative_counterexample is None or len(negative_counterexample) > word_length) and word not in self.returned_counterexamples):
                                negative_counterexample = word

                        self._num_counterexamples_in_EQ += 1

                        # print("positive counterexample:",
                        #       positive_counterexample)
                        # print("negative counterexample:",
                        #       negative_counterexample)
                        break
                        # return word

                # impose bound on word-length
                if(_max_trace_length <= word_length):
                    break

        """ 
        try to return the minimal-size counterexample with alteration
        """

        if(self._last_counterexample_positive):

            if(negative_counterexample is not None):
                self._last_counterexample_positive = False
                return negative_counterexample
            elif(positive_counterexample is not None):
                if(verbose):
                    print("No negative counterexample found")
                return positive_counterexample
        else:

            if(positive_counterexample is not None):
                self._last_counterexample_positive = True
                return positive_counterexample
            elif(negative_counterexample is not None):
                if(verbose):
                    print("No positive counterexample found")
                return negative_counterexample
        return None

    def _ncr(self, n, r):
        r = min(r, n-r)
        numer = reduce(op.mul, range(n, n-r, -1), 1)
        denom = reduce(op.mul, range(1, r+1), 1)
        return numer / denom

    def calculate_revised_delta_and_epsilon(self, verbose=True):
        if(verbose):
            print("Number of samples:", self._number_of_samples)
            print("Number of counterexamples returned:",
                  self._num_counterexamples_in_EQ)

        try:
            _computed_combination = self._ncr(
                self._number_of_samples, self._num_counterexamples_in_EQ)
        except:
            return None, None

        try:
            _new_delta = _computed_combination * \
                math.pow(math.e, -(self.epsilon *
                                   (self._number_of_samples-self._num_counterexamples_in_EQ)))
        except:
            _new_delta = None

        try:
            _new_epsilon = (math.log(_computed_combination)-math.log(self.delta)) / \
                (self._number_of_samples-self._num_counterexamples_in_EQ)
        except:
            _new_epsilon = None

        return _new_delta, _new_epsilon

    def membership_query(self, w):
        return self.specification_dfa.is_word_in(w)

    # @profile
    def teach(self, learner, traces, timeout=20, verbose=True):
        # with timeout(time):
        
        verifier_time = 0
        learner_time = 0
        start_time = time.time()

        for i in range(300):

            if(learner.current_formula_depth > self.max_formula_depth):
                if(verbose):
                    print("Max formula depth achieved")
                return learner, False, learner_time, verifier_time
            """  
                For LTL learning, initialize  a process
                """
            q = Queue()
            p = Process(target=learner.learn_ltlf_and_dfa, args=(q,))
            learning_start_time = time.time()
            p.start()
            p.join(timeout=max(0.5, timeout-(learning_start_time-start_time)))
            p.terminate()
            while p.exitcode == None:
                time.sleep(1)
            if p.exitcode == 0:

                if(verbose):
                    equivalence_test_start_time = time.time()
                    learner_time += equivalence_test_start_time - learning_start_time
                    print("Learning took: ", equivalence_test_start_time -
                          learning_start_time, " s")
                [learner] = q.get()

                # learner.learn_ltlf_and_dfa()
                counterexample = self.equivalence_query(
                    learner.dfa, verbose=verbose)

                if(verbose):
                    verifier_time += time.time() - equivalence_test_start_time
                    print("EQ test took ", time.time() -
                          equivalence_test_start_time, " s")
                if counterexample is None:
                    return learner,  True, learner_time, verifier_time
                else:
                    self.returned_counterexamples.append(counterexample)

                if(self.query_dfa is None):
                    if(self.specification_dfa.classify_word(counterexample)):
                        if(verbose):

                            print("new counterexample:", counterexample,
                                  " should be accepted by implementation")
                        traces.add_positive_example(counterexample)
                    else:
                        if(verbose):

                            print("new counterexample:", counterexample,
                                  " should be rejected by implementation")
                        traces.add_negative_example(counterexample)
                else:
                    if(self.specification_dfa.classify_word(counterexample) and self.query_dfa.classify_word(counterexample)):
                        if(verbose):

                            print("new counterexample:", counterexample,
                                  " should be accepted by implementation")

                        traces.add_positive_example(counterexample)
                    else:
                        if(verbose):

                            print("new counterexample:", counterexample,
                                  " should be rejected by implementation")

                        traces.add_negative_example(counterexample)
            else:
                return learner, False, learner_time, verifier_time

            print(i, " iteration complete\n\n\n")

        return learner, False, learner_time, verifier_time

        # break

    # n > (log(delta) -num_round) / log(1-epsilon)
