import dynet_config
# Set some parameters manualy
dynet_config.set(mem=4000, random_seed=9)
# from GRU import GRUNetwork
from RNN2DFA.LSTM import LSTMNetwork
from RNN2DFA.RNNClassifier import RNNClassifier
from RNN2DFA.Training_Functions import mixed_curriculum_train
import Tomita_Grammars
from RNN2DFA.Training_Functions import make_test_set, make_train_set_for_target
from RNNexplainer import Explainer
import pandas as pd
import LTL2DFA as ltlf2dfa
import time
from sklearn.model_selection import train_test_split
import specific_examples
import argparse


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


# for each example, specify a different generating function


if(target_formula == "balanced parentheses"):
    train_set = generator_dfa.get_balanced_parantheses_train_set(8000, 2, 50, max_train_samples_per_length=3000,
                                                                 search_size_per_length=2000, lengths=[i+1 for i in range(50)])


elif(target_formula == "email match"):
    train_set = make_train_set_for_target(generator_dfa.classify_word, alphabet, lengths=[i+1 for i in range(50)],
                                          max_train_samples_per_length=1000,
                                          search_size_per_length=3000, deviation=200)

    # generate more examples that match the regular expression
    matching_strings = generator_dfa.generate_matching_strings(
        n=10800, max_length=50)
    for string in matching_strings:
        train_set[string] = True


elif(target_formula == "alternating bit protocol"):
    train_set = make_train_set_for_target(generator_dfa.classify_word, alphabet, lengths=[i+1 for i in range(50)],
                                          max_train_samples_per_length=1000,
                                          search_size_per_length=3000, deviation=250)

    # generate more examples that match the regular expression
    matching_strings = generator_dfa.generate_matching_strings(
        n=105000, max_sequence_length=50)
    for string in matching_strings:
        train_set[string] = True

else:
    train_set = make_train_set_for_target(generator_dfa.classify_word, alphabet, lengths=[i+1 for i in range(50)],
                                          max_train_samples_per_length=100,
                                          search_size_per_length=300, deviation=20)


# print ratio
cnt = 0
examples_per_length = [0 for i in range(51)]
for key in train_set:
    if(train_set[key]):
        cnt += 1
    examples_per_length[len(key)] += 1

total_samples = len(train_set)
print("out of ", total_samples, " sequences", cnt,
      " are positive. (percent: ", float(cnt/total_samples), ")")
print("examples per length:", examples_per_length)

# save generated instances
saved_sequences = train_set

# split train:test
X, y = dict2lists(train_set)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.1, random_state=42)
train_set = lists2dict(X_train, y_train)
test_set = lists2dict(X_test, y_test)
train_set_size = len(train_set)
test_set_size = len(test_set)
print("size of train set:", train_set_size)
print("size of test set:", test_set_size)


# define rnn
rnn = RNNClassifier(alphabet, num_layers=3,
                    hidden_dim=10, RNNClass=LSTMNetwork)


# train the model
mixed_curriculum_train(rnn, train_set, stop_threshold=0.0005)
rnn.renew()
dfa_from_rnn = rnn
# statistics

# free train_set
train_set = {}


def percent(num, digits=2):
    tens = pow(10, digits)
    return int(100*num*tens)/tens


print("testing on train set, i.e. test set is train set")
# we're printing stats on the train set for now, but you can define other test sets by using
# make_train_set_for_target

pos = 0
rnn_target = 0
for w in test_set:
    if generator_dfa.classify_word(w):
        pos += 1

    if dfa_from_rnn.classify_word(w) == generator_dfa.classify_word(w):
        rnn_target += 1
test_acc = percent(rnn_target/test_set_size)
print("rnn score against target on test set:                             ",
      rnn_target, "("+str(test_acc)+")")

test_set = {}

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

    performance_explanation_with_rnn = performance_rnn_with_groundtruth = performance_explanation_with_groundtruth = 0

    test_set_size = 0

    for w in saved_sequences:
        if(query_dfa.classify_word(w)):
            test_set_size += 1
            verdict_rnn = dfa_from_rnn.classify_word(w)
            verdict_target = generator_dfa.classify_word(w)
            verdict_ltl = explainer.dfa.classify_word(w)

            if verdict_rnn == verdict_ltl:
                performance_explanation_with_rnn += 1
            if verdict_rnn == verdict_target:
                performance_rnn_with_groundtruth += 1
            if verdict_ltl == verdict_target:
                performance_explanation_with_groundtruth += 1

    if(test_set_size != 0):
        print("Explanation matches RNN:", str(
            percent(performance_explanation_with_rnn/test_set_size)))

        print("RNN matches ground truth:", str(
            percent(performance_rnn_with_groundtruth/test_set_size)))

        print("Explanation matches ground truth:", str(
            percent(performance_explanation_with_groundtruth/test_set_size)))

    fout.close()

    # report in a pandas file
    result = pd.DataFrame(columns=['target',
                                   'query',
                                   'explanation',
                                   'status',
                                   'test accuracy',
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

    if(test_set_size != 0):
        result = result.append(
            {
                'target': target_formula,
                'query': query_formula,
                'explanation': explainer.ltl,
                'status': flag,
                'test accuracy': test_acc,
                'rnn score': percent(performance_rnn_with_groundtruth/test_set_size),
                'explanation score': percent(performance_explanation_with_rnn/test_set_size),
                'explanation score on ground truth': percent(performance_explanation_with_groundtruth/test_set_size),
                'extraction time': end_time-start_time,
                'revised delta': new_delta,
                'revised epsilon': new_epsilon,
                'counterexamples': teacher.returned_counterexamples,
                'train size': len(train_set),
                'test size': len(test_set)
            }, ignore_index=True
        )
    else:
        result = result.append(
            {
                'target': target_formula,
                'query': query_formula,
                'explanation': explainer.ltl,
                'status': flag,
                'test accuracy': test_acc,
                'rnn score': None,
                'explanation score': None,
                'explanation score on ground truth': None,
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
