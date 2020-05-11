import argparse
import specific_examples
from sklearn.model_selection import train_test_split
import time
import LTL2DFA as ltlf2dfa
import pandas as pd
from RNNexplainer import Explainer
from RNN2DFA.Training_Functions import make_test_set, make_train_set_for_target
import Tomita_Grammars
from RNN2DFA.Training_Functions import mixed_curriculum_train
from RNN2DFA.RNNClassifier import RNNClassifier
from RNN2DFA.LSTM import LSTMNetwork
import dynet_config
# Set some parameters manualy
dynet_config.set(mem=2000, random_seed=9)
# from GRU import GRUNetwork


def dict2lists(dictionary):
    X, y = [], []
    for key in dictionary:
        X.append(key)
        y.append(dictionary[key])
    return X, y


def lists2dict(x, y):
    # both x and y should have same length
    assert len(x) == len(y), "Error dimension"
    d = {}
    n = len(x)
    for idx in range(n):
        d[x[idx]] = y[idx]
    return d


# distribute tasks among mpi-processes
parser = argparse.ArgumentParser()
parser.add_argument("--thread", help="index of thread", default=0, type=int)
args = parser.parse_args()
thread = args.thread


# get example to test
generator_dfa = None
try:
    generator_dfa = eval("specific_examples.Example" +
                         str(thread+1)+"(token="+str(thread)+")")
    if(thread == 0):
        generator_dfa = specific_examples.Email()
    elif(thread == 1):
        generator_dfa = specific_examples.Balanced_Parentheses()
    elif(thread == 2):
        generator_dfa = specific_examples.Alternating_Bit_Protocol()

except:
    exit()
target_formula = generator_dfa.target_formula
alphabet = generator_dfa.alphabet
query_formulas = generator_dfa.query_formulas


timeout = 400


# make training sets
if(target_formula != "balanced parentheses"):
    train_set = make_train_set_for_target(generator_dfa.classify_word, alphabet,
                                          max_train_samples_per_length=10000,
                                          search_size_per_length=30000)
else:
    train_set = generator_dfa.get_balanced_parantheses_train_set(15000, 2, 20)
    print(train_set)

# generate more examples that match the regular expression
if(target_formula == "email match"):
    matching_strings = generator_dfa.generate_matching_strings(
        n=2000, max_length=20)
    for string in matching_strings:
        train_set[string] = True


# split train:test
X, y = dict2lists(train_set)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
train_set = lists2dict(X_train, y_train)
test_set = lists2dict(X_test, y_test)


# define rnn
rnn = RNNClassifier(alphabet, num_layers=2,
                    hidden_dim=10, RNNClass=LSTMNetwork)


# train the model
mixed_curriculum_train(rnn, train_set, stop_threshold=0.0005)
rnn.renew()
dfa_from_rnn = rnn
# statistics


def percent(num, digits=2):
    tens = pow(10, digits)
    return int(100*num*tens)/tens


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
        alphabet=[character for character in alphabet], formula=query_formula, token=str(thread))

    """  
    Create initial samples
    """

    from RNNexplainer import Traces
    traces = Traces(rnn, alphabet, token=str(thread))
    traces.label_from_network([])
    traces.write_in_file(location='dummy.trace')

    from PACTeacher.pac_teacher import PACTeacher as Teacher
    explainer = Explainer(
        alphabet=[character for character in alphabet], token=str(thread))
    teacher = Teacher(dfa_from_rnn, epsilon=.05, delta=.05,
                      max_trace_length=50, max_formula_depth=50, query_dfa=query_dfa)

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
    new_delta = None
    new_epsilon = None
    if(not flag):
        fout.write(" [incomplete]")
        print("incomplete formula")
        new_delta, new_epsilon = teacher.calculate_revised_delta_and_epsilon()
        print(new_delta, new_epsilon)

    print("\nTime taken:", end_time-start_time)
    fout.close()
    fout = open("output/log.txt", "a")

    performance_ltl_wo_query = performance_ltl_with_target_wo_query = performance_ltl = performance_ltl_with_target = 0

    for w in test_set:
        verdict_rnn = dfa_from_rnn.classify_word(w)
        verdict_target = generator_dfa.classify_word(w)
        verdict_query = query_dfa.classify_word(w)
        verdict_ltl = explainer.dfa.classify_word(w)
        if verdict_rnn == verdict_ltl:
            performance_ltl_wo_query += 1
        if verdict_ltl == verdict_target:
            performance_ltl_with_target_wo_query += 1
        if (verdict_rnn and verdict_query) == verdict_ltl:
            performance_ltl += 1
        if verdict_ltl == (verdict_target and verdict_query):
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
                                   'extraction time',
                                   'revised delta',
                                   'revised epsilon',
                                   'counterexamples',
                                   'train size',
                                   'test size'
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
            'extraction time': end_time-start_time,
            'revised delta': new_delta,
            'revised epsilon': new_epsilon,
            'counterexamples': teacher.returned_counterexamples,
            'train size': len(train_set),
            'test size': len(test_set)
        }, ignore_index=True
    )
    print(result.to_string(index=False))
    result.to_csv('output/result.csv', header=False, index=False, mode='a')
