from RNN2DFA.LSTM import LSTMNetwork
from RNN2DFA.GRU import GRUNetwork
from RNN2DFA.Extraction import extract
from RNN2DFA.RNNClassifier import RNNClassifier
from RNN2DFA.Training_Functions import mixed_curriculum_train
from RNN2DFA.Training_Functions import make_test_set, make_train_set_for_target
from RNNexplainer import Explainer
import pandas as pd
import LTL2DFA as ltlf2dfa
import time
from sklearn.model_selection import train_test_split
import specific_examples
import argparse
import os.path
import pickle
from pythomata import SimpleDFA
import random
from samples2ltl.utils.Traces import Trace
# parameters

timeout = 400
maximum_sequence_length = 50
maximum_formula_depth = 50
epsilons = [0.05]
deltas = [0.05]
RNNClass = LSTMNetwork
run_lstar = True

# network parameters:
num_layers = 2
num_hidden_dim = 10
input_dim = 3
iterations = 1
stop_threshold = 0.0005


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
parser.add_argument("--demo", action='store_true')
parser.add_argument("--random", action='store_true')
args = parser.parse_args()
thread = args.thread
random_run = args.random





if(random_run):
    print("Running in random mode")
    iterations = 100
    epsilons = [0.05]
    deltas = [0.05]


# get example to test
generator_dfa = None
try:
    if(args.demo):
        generator_dfa = eval("specific_examples.Example" +
                             str(thread+1)+"(token="+str(thread)+")")
    else:
        if(thread % 6 == 0):
            num_layers = 3
            generator_dfa = specific_examples.Email()
        elif(thread % 6 == 1):
            num_layers = 3
            generator_dfa = specific_examples.Balanced_Parentheses()
        elif(thread % 6 == 2):
            num_layers = 3
            generator_dfa = specific_examples.Alternating_Bit_Protocol()
        elif(thread % 6 == 3):
            generator_dfa = eval("specific_examples.Example" +
                                 str(4)+"(token="+str(thread)+")")
        elif(thread % 6 == 4):
            generator_dfa = eval("specific_examples.Example" +
                                 str(2)+"(token="+str(thread)+")")
        elif(thread % 6 == 5):
            generator_dfa = eval("specific_examples.Example" +
                                 str(6)+"(token="+str(thread)+")")


except:
    exit()
target_formula = generator_dfa.target_formula
alphabet = generator_dfa.alphabet
query_formulas = generator_dfa.query_formulas

# for each example, specify different parameters random words generating function
file_name = "benchmarks/" + target_formula.replace(" ", "_")+".pkl"

if not os.path.isfile(file_name):

    if(target_formula == "balanced parentheses"):

        train_set = generator_dfa.get_balanced_parantheses_train_set(8000, 2, 50, max_train_samples_per_length=3000,
                                                                     search_size_per_length=2000, lengths=[i for i in range(maximum_sequence_length+1)])

    elif(target_formula == "email match"):

        train_set = make_train_set_for_target(generator_dfa.classify_word, alphabet, lengths=[i for i in range(maximum_sequence_length+1)],
                                              max_train_samples_per_length=1000,
                                              search_size_per_length=3000, deviation=200)

        # generate more examples that match the regular expression
        matching_strings = generator_dfa.generate_matching_strings(
            n=10800, max_length=50)
        for string in matching_strings:
            train_set[string] = True

    elif(target_formula == "alternating bit protocol"):

        train_set = make_train_set_for_target(generator_dfa.classify_word, alphabet, lengths=[i for i in range(maximum_sequence_length+1)],
                                              max_train_samples_per_length=1000,
                                              search_size_per_length=3000, deviation=250)

        # generate more examples that match the regular expression
        matching_strings = generator_dfa.generate_matching_strings(
            n=105000, max_sequence_length=50)
        for string in matching_strings:
            train_set[string] = True
    elif(target_formula == 'G(a->X(b))'):
        train_set = make_train_set_for_target(generator_dfa.classify_word, alphabet, lengths=[i for i in range(maximum_sequence_length+1)],
                                              max_train_samples_per_length=1000,
                                              search_size_per_length=3000, deviation=20)

    else:
        train_set = make_train_set_for_target(generator_dfa.classify_word, alphabet, lengths=[i for i in range(maximum_sequence_length+1)],
                                              max_train_samples_per_length=10000,
                                              search_size_per_length=30000, deviation=20)

    # now save the dataset to file
    with open(file_name, "wb") as f:
        pickle.dump(train_set, f, pickle.HIGHEST_PROTOCOL)

else:
    # load the dataset
    print("loading from previously stored benchmarks")

    def load_obj(name):
        with open(name, "rb") as f:
            return pickle.load(f)
    train_set = load_obj(file_name)

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

# split train:test
X, y = dict2lists(train_set)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42)
train_set = lists2dict(X_train, y_train)
test_set = lists2dict(X_test, y_test)
train_set_size = len(train_set)
test_set_size = len(test_set)

# intentionally pushing "" (empty string) in train_set
if('' not in train_set):
    train_set[''] = test_set['']
    print("Empty string status:", train_set[''])
else:
    print("Empty string was already included in train set")
    print("Empty string status:", train_set[''])

print("size of train set:", train_set_size)
print("size of test set:", test_set_size)

print("configurations: layers: ", num_layers,
          "hidden dimension: ", num_hidden_dim,
          "input dim: ", input_dim,
          "network: ", RNNClass,
          "stop threshold: ", stop_threshold)


# define rnn
rnn = RNNClassifier(alphabet, num_layers=num_layers,
                    hidden_dim=num_hidden_dim, RNNClass=RNNClass, input_dim=input_dim, target=target_formula)

try:
    # train the model
    if not os.path.isfile("model/"+target_formula+".model"):
        mixed_curriculum_train(rnn, train_set, stop_threshold=stop_threshold)
        rnn.save_model()
    else:
        print("loading already saved model")
        rnn.load_model()
except:
    print("Training error: however moving on as life also goes on" )
    
rnn.renew()
dfa_from_rnn = rnn
# statistics

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



for iteration in range(iterations):
    print("##################################### iteration",
          iteration, "     ######################")

    
    
    
    for epsilon in epsilons:
        for delta in deltas:
            for query_formula in query_formulas:
                dfa_from_rnn.renew()

                print("target:", target_formula)
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

                # LTL learner
                from PACTeacher.pac_teacher import PACTeacher as Teacher
                explainer = Explainer(
                    alphabet=[character for character in alphabet], token=str(thread))
                teacher = Teacher(dfa_from_rnn, epsilon=epsilon, delta=delta,
                                  max_trace_length=maximum_sequence_length, max_formula_depth=maximum_formula_depth, query_dfa=query_dfa)

                start_time = time.time()
                from multiprocessing import Process, Queue
                explainer, flag, learner_time, verifier_time = teacher.teach(
                    explainer, traces, timeout=timeout)
                end_time = time.time()
                print("\n\nepsilon=", teacher.epsilon, "delta=", teacher.delta,
                      "max_trace_length=", teacher.max_trace_length)
                print("query:", query_formula)
                print("final ltl: ", explainer.ltl)

                new_delta = None
                new_epsilon = None
                if(not flag):
                    print("incomplete formula")
                    new_delta, new_epsilon = teacher.calculate_revised_delta_and_epsilon()
                    print(new_delta, new_epsilon)

                print("time learner:", learner_time)
                print('time verifier:', verifier_time)
                print("Random words:", teacher.number_of_words_checked)


                print("\nTime taken to extract ltl:", end_time-start_time)
                
                # DFA learner
                if(run_lstar):
                    print("\n\n\n\n\n")
                    dfa_from_rnn.renew()
                    start_time_lstar = time.time()
                    # try:
                    dfa_lstar, lstar_flag = extract(rnn, query=query_dfa, max_trace_length=maximum_sequence_length, epsilon=delta,
                                                        delta=delta, time_limit=timeout, initial_split_depth=10, starting_examples=[])
                    end_time_lstar = time.time()

                    dfa_lstar.draw_nicely(
                        filename=str(thread)+"_" + str(iteration)+"_" + target_formula+":"+query_formula+"_"+str(epsilon)+"_"+str(delta))
                    print("\nTime taken to extract lstar-dfa:",
                            end_time_lstar-start_time_lstar)
                    print("number of states of the dfa:", len(dfa_lstar.Q))
                    print("returned flag:", lstar_flag)
                    print("transitions:->")
                    print(dfa_lstar.delta)
                    num_lstar_states = len(dfa_lstar.Q)

                performance_explanation_with_rnn = performance_rnn_with_groundtruth = performance_explanation_with_groundtruth = 0
                lstar_performance_explanation_with_rnn = lstar_performance_explanation_with_groundtruth = 0

                num_positive_examples = 0
                num_negative_examples = 0
                
                test_set_size = 0
                for w in test_set:
                    
                    dfa_from_rnn.renew()

                    test_set_size += 1
                    verdict_rnn = dfa_from_rnn.classify_word(w)
                    verdict_target = generator_dfa.classify_word(w)
                    trace_vector = []
                    for letter in w:
                        trace_vector.append([alphabet[i] == letter for i in range(len(alphabet))])
                    trace = Trace(trace_vector)
                    if(len(w) == 0):
                        trace = Trace([[False for _ in alphabet]])
                    verdict_ltl = trace.evaluateFormulaOnTrace(explainer.formula)
                    verdict_query = query_dfa.classify_word(w)

                    if(run_lstar):
                        verdict_lstar = dfa_lstar.classify_word(w)

                    if (verdict_rnn and verdict_query) == verdict_ltl:
                        performance_explanation_with_rnn += 1
                    if verdict_rnn == verdict_target:
                        performance_rnn_with_groundtruth += 1
                    if verdict_ltl == (verdict_target and verdict_query):
                        performance_explanation_with_groundtruth += 1
                    if(run_lstar):
                        if (verdict_rnn and verdict_query) == verdict_lstar:
                            lstar_performance_explanation_with_rnn += 1
                        if verdict_lstar == (verdict_target and verdict_query):
                            lstar_performance_explanation_with_groundtruth += 1

                if(test_set_size != 0):
                    print("Explanation matches RNN:", str(
                        percent(performance_explanation_with_rnn/test_set_size)))

                    print("RNN matches ground truth:", str(
                        percent(performance_rnn_with_groundtruth/test_set_size)))

                    print("Explanation matches ground truth:", str(
                        percent(performance_explanation_with_groundtruth/test_set_size)))

                    if(run_lstar):
                        print("Lstar matches RNN:", str(
                            percent(lstar_performance_explanation_with_rnn/test_set_size)))

                        print("Lstar matches ground truth:", str(
                            percent(lstar_performance_explanation_with_groundtruth/test_set_size)))

                
                if(not (run_lstar)):
                    num_lstar_states = None
                    start_time_lstar = 0
                    end_time_lstar = 0
                    lstar_performance_explanation_with_rnn = 0
                    lstar_performance_explanation_with_groundtruth = 0
                    lstar_flag = False

                # report in a pandas file
                result = pd.DataFrame(columns=['thread',
                                                'target',
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
                                               'test size',
                                               'ltl_depth',
                                               'lstar_states',
                                               'lstar explanation score',
                                               'lstar explanation score on ground truth',
                                               'lstar extraction time',
                                               'lstar_status',
                                               'epsilon',
                                               'delta', 
                                               'learner time', 
                                               'verifier time', 
                                               'random words'
                                               ])

                if(test_set_size != 0):
                    result = result.append(
                        {
                            'thread':thread,
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
                            'train size': train_set_size,
                            'test size': test_set_size,
                            "ltl_depth": explainer.formula_depth,
                            "lstar_states": num_lstar_states,
                            'lstar explanation score': percent(lstar_performance_explanation_with_rnn/test_set_size),
                            'lstar explanation score on ground truth': percent(lstar_performance_explanation_with_groundtruth/test_set_size),
                            'lstar extraction time': end_time_lstar - start_time_lstar,
                            'lstar_status': lstar_flag,
                            'epsilon': epsilon,
                            'delta': delta,
                            'learner time': learner_time, 
                            'verifier time': verifier_time, 
                            'random words': teacher.number_of_words_checked


                        }, ignore_index=True
                    )
                else:
                    result = result.append(
                        {
                            'thread':thread,
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
                            'train size': train_set_size,
                            'test size': test_set_size,
                            "ltl_depth": explainer.formula_depth,
                            "lstar_states": num_lstar_states,
                            'lstar explanation score': None,
                            'lstar explanation score on ground truth': None,
                            'lstar extraction time': end_time_lstar - start_time_lstar,
                            'lstar_status': lstar_flag,
                            'epsilon': epsilon,
                            'delta': delta,
                            'learner time': learner_time, 
                            'verifier time': verifier_time, 
                            'random words': teacher.number_of_words_checked


                        }, ignore_index=True
                    )
                print(result.to_string(index=False))
                result.to_csv('output/result.csv', header=False,
                              index=False, mode='a')
