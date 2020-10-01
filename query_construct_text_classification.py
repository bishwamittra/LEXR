import numpy as np
from sklearn.model_selection import StratifiedKFold
from RNNexplainer import Traces, Explainer
import re

skf = StratifiedKFold(n_splits=200)
def dict2lists(dictionary):
    X,y=[],[]
    for key in dictionary:
        X.append(key)
        y.append(dictionary[key])
    return X,y


from specific_examples import Text_Classification
tc = Text_Classification()
alphabet = tc.alphabet
X,y = dict2lists(tc.dict)
X = np.array(X)
y = np.array(y)
skf.get_n_splits(X, y)
print(skf)



queries = []
simple_ltls = []
for train_index, test_index in skf.split(X, y):
    _, X_test = X[train_index], X[test_index]
    # y_train, y_test = y[train_index], y[test_index]c

    traces=Traces(tc, alphabet, token="bal")
    traces.label_from_network(X_test,learn=True)
    traces.write_in_file()
    query_creater=Explainer(alphabet=[character for character in alphabet], token="bal")
    query_creater.learn_ltlf_and_dfa(python_processing=False)

    indices = re.findall(r'\d+', query_creater.ltl)
    ltl = query_creater.ltl
    for index in indices:
        if(index != "0"):
            ltl = ltl.replace("x" + index, tc.tok.index_word[int(index)])
        else:
            ltl = ltl.replace("x" + index, "NuLL")
    
    queries.append(str(query_creater.ugly_ltl))
    simple_ltls.append(ltl)
    f = open("benchmarks/query_spam.txt", 'w')
    f.write(str(queries))
    f.close()
    print(ltl)
    print(queries)