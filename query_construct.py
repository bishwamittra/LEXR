import numpy as np
from sklearn.model_selection import StratifiedKFold
from lexr.RNNexplainer import Traces, Explainer
import re
import argparse
import pickle
import os
from tqdm import tqdm


def dict2lists(dictionary):
    X,y=[],[]
    for key in dictionary:
        X.append(key)
        y.append(dictionary[key])
    return X,y

parser = argparse.ArgumentParser()
parser.add_argument("--benchmarks",  default='Example4', type=str)
args = parser.parse_args()


from lexr.specific_examples import *
benchmarks = eval(args.benchmarks +"(token=" + args.benchmarks + ")")
alphabet = benchmarks.alphabet
file_name = "benchmarks/" + benchmarks.target_formula.replace(" ", "_")+".pkl"

train_set = None

try:
    def load_obj(name):
        with open(name, "rb") as f:
            return pickle.load(f)
    train_set = load_obj(file_name)
except Exception as e:
    print(e)
    exit()

if(args.benchmarks == "Example3"):
    skf = StratifiedKFold(n_splits=50)
else:
    skf = StratifiedKFold(n_splits=200)
X,y = dict2lists(train_set)
X = np.array(X)
y = np.array(y)
skf.get_n_splits(X, y)

os.system("mkdir -p benchmarks/query/")

queries = []
for train_index, test_index in skf.split(X, y):
    try:
        _, X_test = X[train_index], X[test_index]
        # y_train, y_test = y[train_index], y[test_index]c

        traces=Traces(benchmarks, alphabet, token=args.benchmarks)
        traces.label_from_network(X_test,learn=True)
        traces.write_in_file()
        query_creater=Explainer(alphabet=[character for character in alphabet], token=args.benchmarks)
        query_creater.learn_ltlf_and_dfa(python_processing=False, verbose=False)
        
        # indices = re.findall(r'\d+', query_creater.ltl)
        # ltl = query_creater.ltl
        # for index in indices:
        #     if(index != "0"):
        #         ltl = ltl.replace("x" + index, tc.tok.index_word[int(index)])
        #     else:
        #         ltl = ltl.replace("x" + index, "NuLL")
        
        queries.append(str(query_creater.ugly_ltl))
        f = open("benchmarks/query/" + benchmarks.target_formula.replace(" ", "_") + ".txt", 'w')
        f.write(str(queries))
        f.close()
    except:
        pass
    # break
