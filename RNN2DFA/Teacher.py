from RNN2DFA.Quantisations import SVMDecisionTreeQuantisation
from RNN2DFA.WhiteboxRNNCounterexampleGenerator import WhiteboxRNNCounterexampleGenerator
from time import time
import numpy as np
from PACTeacher import pac_teacher
from multiprocessing import Process, Queue
from samples2ltl.utils.Traces import Trace

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
        # print(words)
        self.recorded_words.update(
            {w: self.classify_word(w) for w in words})

    def classify_word(self, w):
        # this is modified to icorporate query
        trace_vector = []
        if("x" in w):
            word = w.split("x")[1:]
            for letter in word:
                trace_vector.append([self.alphabet[i] == "x" + letter for i in range(len(self.alphabet))])
        else:
            for letter in w:
                trace_vector.append([self.alphabet[i] == letter for i in range(len(self.alphabet))])

        if(len(w) == 0):
            trace = Trace([[False for _ in self.alphabet]])
        else:
            trace = Trace(trace_vector)
        return self.network.classify_word(w) and trace.evaluateFormulaOnTrace(self.query)

    def equivalence_query(self, dfa):
        self.dfas.append(dfa)
        start = time()
        # call pac equivalence query
        counterexample = self.pac_teacher.equivalence_query(dfa, verbose=False, evaluate_DFA=True)
        self.pac_teacher.returned_counterexamples.append(counterexample)
        
        
        # counterexample,message = self.counterexample_generator.counterexample(dfa)
        counterexample_time = time() - start
        # print("equivalence checking took: " + str(counterexample_time))
        if not None is counterexample:
            print("Returned counterexample is:", counterexample, " which should be classified: ", self.classify_word(counterexample))
            self.counterexamples_with_times.append(
                (counterexample, counterexample_time))
            return counterexample
        return None
