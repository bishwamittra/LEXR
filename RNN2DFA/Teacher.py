from RNN2DFA.Quantisations import SVMDecisionTreeQuantisation
from RNN2DFA.WhiteboxRNNCounterexampleGenerator import WhiteboxRNNCounterexampleGenerator
from time import clock
import numpy as np
from PACTeacher import pac_teacher


class Teacher:
    def __init__(self, network, query, num_dims_initial_split=10, starting_examples=None, epsilon=0.05, delta=0.05, max_trace_length=20, ):
        if None is starting_examples:
            starting_examples = []
        # observation table uses this as its T (according to angluin paper terminology)
        self.recorded_words = {}
        self.discretiser = SVMDecisionTreeQuantisation(num_dims_initial_split)
        # self.counterexample_generator = WhiteboxRNNCounterexampleGenerator( network, self.discretiser, starting_examples)
        self.dfas = []
        self.counterexamples_with_times = []
        self.current_ce_count = 0
        self.network = network
        # this is more for intuitive use by lstar (it doesn't need to know there's a network involved)
        self.alphabet = network.alphabet

        # following are added to implement pac-equivalence query

        self.query = query
        self.pac_teacher = pac_teacher.PACTeacher(
            network, epsilon, delta, max_trace_length=max_trace_length, max_formula_depth=None, query_dfa=query)
    def update_words(self, words):
        seen = set(self.recorded_words.keys())
        # need this to avoid answering same thing twice, which may happen a lot now with optimistic querying...
        words = set(words) - seen
        self.recorded_words.update(
            {w: self.network.classify_word(w) for w in words})

    def classify_word(self, w):
        # this is modified to incorporate query
        return self.network.classify_word(w) and self.query.classify_word(w)

    def equivalence_query(self, dfa):
        self.dfas.append(dfa)
        start = clock()
        # call pac equivalence query
        counterexample = self.pac_teacher.equivalence_query(dfa, verbose=True)
        self.pac_teacher.returned_counterexamples.append(counterexample)
        
        
        # counterexample,message = self.counterexample_generator.counterexample(dfa)
        counterexample_time = clock() - start
        # print("equivalence checking took: " + str(counterexample_time))
        if not None is counterexample:
            print("Returned counterexample is:", counterexample, " which should be classified: ", self.classify_word(counterexample))
            self.counterexamples_with_times.append(
                (counterexample, counterexample_time))
            return counterexample
        return None
