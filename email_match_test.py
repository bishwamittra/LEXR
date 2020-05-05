

from RNN2DFA.LSTM import LSTMNetwork
# from GRU import GRUNetwork
from RNN2DFA.RNNClassifier import RNNClassifier
from RNN2DFA.Training_Functions import mixed_curriculum_train
import Tomita_Grammars
from RNN2DFA.Training_Functions import make_test_set, make_train_set_for_target
from RNNexplainer import Explainer
import pandas as pd
import LTL2DFA as ltlf2dfa
import time


from specific_examples import Email
email = Email()
generator_dfa = email  # to make everything work
target_formula = email.target_formula
alphabet = email.alphabet


""" 
email symbol description
----

numerical symbols: m, n
letters: p, q, r
a [@] 
d [dot]

---
Regex: (letters)(letters+numerical)+@(letters)d
"""


timeout = 400


query_formulas = [
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
    "~(F(m|n)->((p|q|r)U(m|n)))"  # opposite to the earlier query

]


# make training sets
train_set = make_train_set_for_target(generator_dfa.classify_word, alphabet,
                                      max_train_samples_per_length=100000,
                                      search_size_per_length=300000)

# generate more examples that match the regular expression
if(target_formula == "email match"):
    matching_strings = email.generate_matching_strings(n=2000, max_length=20)
    for string in matching_strings:
        train_set[string] = True


# define rnn
rnn = RNNClassifier(alphabet, num_layers=5,
                    hidden_dim=10, RNNClass=LSTMNetwork)


# train the model
mixed_curriculum_train(rnn, train_set, stop_threshold=0.0005)
rnn.renew()
dfa_from_rnn = rnn
# statistics


def percent(num, digits=2):
    tens = pow(10, digits)
    return int(100*num*tens)/tens


test_set = train_set
print("testing on train set, i.e. test set is train set")
# we're printing stats on the train set for now, but you can define other test sets by using
# make_train_set_for_target

n = len(test_set)
print("test set size:", n)
pos = 0
rnn_target = 0
for w in test_set:
    if generator_dfa.classify_word(w):
        pos += 1

    if dfa_from_rnn.classify_word(w) == generator_dfa.classify_word(w):
        rnn_target += 1
print("rnn score against target on test set:                             ",
      rnn_target, "("+str(percent(rnn_target/n))+")")


for query_formula in query_formulas:

    print("query:", query_formula)

    # use a query LTL formula
    query_dfa = ltlf2dfa.translate_ltl2dfa(
        alphabet=[character for character in alphabet], formula=query_formula)

    """  
    Create initial samples
    """

    test_set = []
    if(query_dfa is None):
        query_formula = None
        test_set = make_test_set(alphabet)
        raise SystemError

    from RNNexplainer import Traces
    traces = Traces(rnn, alphabet)
    traces.label_from_network(test_set)
    traces.write_in_file()

    from PACTeacher.pac_teacher import PACTeacher as Teacher
    explainer = Explainer(alphabet=[character for character in alphabet])
    teacher = Teacher(dfa_from_rnn, epsilon=.05, delta=.05,
                      max_trace_length=20, max_formula_depth=10, query_dfa=query_dfa)

    start_time = time.time()
    from multiprocessing import Process, Queue
    explainer, flag = teacher.teach(explainer, traces, timeout=timeout)
    end_time = time.time()
    print("\n\nepsilon=", teacher.epsilon, "delta=", teacher.delta,
          "max_trace_length=", teacher.max_trace_length)
    print("query:", query_formula)
    print("final ltl: ", explainer.ltl)

    fout = open("output/log.txt", "a")
    fout.write("\n\nquery: "+query_formula)
    fout.write("\nfinal LTL: " + explainer.ltl)
    if(not flag):
        fout.write(" [incomplete]")
        print("incomplete formula")
    fout.write("\n\n")

    print("\nTime taken:", end_time-start_time)
    fout.close()
    test_set = train_set
    fout = open("output/log.txt", "a")

    performance_ltl_wo_query = performance_ltl_with_target_wo_query = performance_ltl = performance_ltl_with_target = 0

    for w in test_set:
        if dfa_from_rnn.classify_word(w) == explainer.dfa.classify_word(w):
            performance_ltl_wo_query += 1
        if explainer.dfa.classify_word(w) == generator_dfa.classify_word(w):
            performance_ltl_with_target_wo_query += 1
        if (dfa_from_rnn.classify_word(w)and query_dfa.classify_word(w)) == explainer.dfa.classify_word(w):
            performance_ltl += 1
        if explainer.dfa.classify_word(w) == (generator_dfa.classify_word(w) and query_dfa.classify_word(w)):
            performance_ltl_with_target += 1

    print("extracted LTL score against rnn on test set:                      ",
          performance_ltl_wo_query, "("+str(percent(performance_ltl_wo_query/n))+")")

    print("extracted LTL score against target on rnn's test set:             ",
          performance_ltl_with_target_wo_query, "("+str(percent(performance_ltl_with_target_wo_query/n))+")")

    print("extracted LTL score against rnn on test set (with query):         ",
          performance_ltl, "("+str(percent(performance_ltl/n))+")")

    print("extracted LTL score against target on rnn's test set (with query):",
          performance_ltl_with_target, "("+str(percent(performance_ltl_with_target/n))+")")

    fout.close()

    # report in a pandas file
    result = pd.DataFrame(columns=['target',
                                   'query',
                                   'explanation',
                                   'status',
                                   'rnn score',
                                   'explanation score',
                                   'explanation score on ground truth',
                                   'extraction time'
                                   ])

    result = result.append(
        {
            'target': target_formula,
            'query': query_formula,
            'explanation': explainer.ltl,
            'status': flag,
            'rnn score': percent(rnn_target/n),
            'explanation score': percent(performance_ltl/n),
            'explanation score on ground truth': percent(performance_ltl_with_target/n),
            'extraction time': end_time-start_time
        }, ignore_index=True
    )
    print(result.to_string(index=False))
    result.to_csv('output/result.csv', header=False, index=False, mode='a')
