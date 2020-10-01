import LTLlearner as LTL_learner
import LTL2DFA as DFA_learner
import graphviz
from IPython.display import display
from IPython.display import Image
import pydotplus
import os


class Traces:

    def __init__(self, network, alphabet, token=""):
        self.network = network
        self.alphabet = alphabet
        self.token = token

    def __repr__(self):
        return "Traces:->\n"+'\n'.join(" - %s: %s" % (item, value) for (item, value) in vars(self).items() if "__" not in item)

    def label_from_network(self, dataset, learn=False):
        self.positive_example = []
        self.negative_example = []

        for example in dataset:
            if(self.network.classify_word(example)):
                self.positive_example.append(example)
            else:
                self.negative_example.append(example)

        if(not learn):
            # only consider a fraction of test samples
            self.positive_example = self.positive_example[:1]
            self.negative_example = self.negative_example[:1]

        if(learn):
            l = min(len(self.positive_example), len(self.negative_example))
            for i in range(l):
                self.positive_example[i] = self.positive_example[i].replace("x0", "")
                self.negative_example[i] = self.negative_example[i].replace("x0", "")
    
            self.positive_example = self.positive_example[:l]
            self.negative_example = self.negative_example[:l]



    # auxiliary function
    def _to_trace(self, example, length_alphabet, char_to_int):

        # special case
        if(len(example) == 0):
            return ",".join("0" for _ in range(length_alphabet))

        if("x" in example):
            example = example.split("x")[1:]
            integer_encoded = [char_to_int["x" + char] for char in example]
        else:
            integer_encoded = [char_to_int[char] for char in example]

        # one hot encode
        onehot_encoded = list()
        for value in integer_encoded:
            letter = [0 for _ in range(length_alphabet)]
            letter[value] = 1
            onehot_encoded.append(letter)
        # trace format
        trace = ";".join([",".join(map(str, record))
                          for record in onehot_encoded])

        return trace

    def write_in_file(self, location="dummy.trace", verbose=False):

        if(verbose):
            print("\n\npositive traces---> ")
            print(self.positive_example)
            print("\n\nnegative traces---> ")
            print(self.negative_example)
            print("\n\n")
       
        self.location = location + self.token

        # write positive and negative examples as a traces in a file

        alphabet_length = len(self.alphabet)
        # define a mapping of chars to integers
        char_to_int = dict((c, i) for i, c in enumerate(self.alphabet))
        string = ""
        for example in self.positive_example:
            trace = self._to_trace(example, alphabet_length, char_to_int)
            if(trace != ""):
                string += trace+"\n"
        string += "---\n"
        for example in self.negative_example:
            trace = self._to_trace(example, alphabet_length, char_to_int)
            if(trace != ""):
                string += trace+"\n"
            # print(example, trace)
        fin = open(location + self.token, "w")
        fin.write(string[:-1])
        fin.close()

    def add_positive_example(self, example, write_in_file=True):
        if(example in self.negative_example):
            self.negative_example.remove(example)

        if(not example in self.positive_example):
            self.positive_example.append(example)

        if(write_in_file):
            self.write_in_file()

    def add_negative_example(self, example, write_in_file=True):

        if(example in self.positive_example):
            self.positive_example.remove(example)

        if(not example in self.negative_example):
            self.negative_example.append(example)

        if(write_in_file):
            self.write_in_file()


class Explainer:

    def __init__(self, alphabet, traces="dummy.trace", token=""):
        self.dfa = None
        self.ltl = None
        self.traces = traces + token
        self.alphabet = alphabet
        self.current_formula_depth = 1
        self.token = token
        self.formula = None

    def learn_ltlf_and_dfa(self, queue = None, show_dfa=False, python_processing = True):

        # print(self.token)
        learned_formulas, self.current_formula_depth = LTL_learner.learnLTL(
            self.traces, startDepth=self.current_formula_depth)

        self.formula_depth = learned_formulas[0].getNumberOfSubformulas()
            
        # print("Learning formula with depth", learned_formulas[0].getDepth())
        # print("Number of subformulas:", learned_formulas[0].getNumberOfSubformulas())

        
        try:
            self.ugly_ltl = learned_formulas[0]
            formulas = self._convert_formula(learned_formulas)
            self.ltl = formulas[0]
            self.formula = learned_formulas[0]
        except:
            self.ltl = "false"

        # self.dfa = DFA_learner.translate_ltl2dfa(
        #     alphabet=self.alphabet, formula=self.ltl, token=self.token)

        print("learned LTL formula:", self.ltl)
        # # print(self.dfa)

        # if(show_dfa):
        #     print(self.dfa)
        #     pydot_graph = pydotplus.graph_from_dot_file("automa.dot")
        #     display(Image(pydot_graph.create_png()))

        if(python_processing):
            queue.put([self])

    def _convert_formula(self, learned_formulas):
        # convert propositional variables in LTLf to human readable alphabet
        formulas = []
        for formula in learned_formulas:
            formula = formula.prettyPrint()
            for idx in range(len(self.alphabet)):
                formula = formula.replace('x'+str(idx), self.alphabet[idx])
            formula = formula.replace("!", "~")
            formulas.append(formula)
        return formulas


explainer = Explainer(alphabet=['a', 'b', 'c'])
