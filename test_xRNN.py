import test_samples2ltl as LTL_learner
import test_ltl2dfa as DFA_learner

class Traces:

    def __init__(self, network, alphabet):
        self.network=network
        self.alphabet=alphabet

    def __repr__(self):
        return "Traces:->\n"+'\n'.join(" - %s: %s" % (item, value) for (item, value) in vars(self).items() if "__" not in item)


    def label_from_network(self, dataset):
        self.positive_example=[]
        self.negative_example=[]

        for example in dataset:
            if(self.network.classify_word(example)):
                self.positive_example.append(example)
            else:
                self.negative_example.append(example)

        # only consider a fraction of test samples
        self.positive_example=self.positive_example[:2]
        self.negative_example=self.negative_example[:2]

    # auxiliary function
    def _to_trace(self, example,length_alphabet, char_to_int):

        # special case
        if(len(example)==0):
            return ",".join("0" for _ in range(length_alphabet))


        integer_encoded = [char_to_int[char] for char in example]

            

        # one hot encode
        onehot_encoded = list()
        for value in integer_encoded:
            letter = [0 for _ in range(length_alphabet)]
            letter[value] = 1
            onehot_encoded.append(letter)
        # trace format
        trace=";".join([",".join(map(str, record)) for record in onehot_encoded])

        return trace

    def write_in_file(self, location="dummy.trace"):
        self.location=location

        # write positive and negative examples as a traces in a file

        alphabet_length=len(self.alphabet)
        # define a mapping of chars to integers
        char_to_int = dict((c, i) for i, c in enumerate(self.alphabet))
        string=""
        for example in self.positive_example:
            trace=self._to_trace(example,alphabet_length,char_to_int)
            if(trace != ""):
                string+=trace+"\n"
        string+="---\n"
        for example in self.negative_example:
            trace=self._to_trace(example,alphabet_length,char_to_int)
            if(trace != ""):
                string+=trace+"\n"
            # print(example, trace)
        fin=open("dummy.trace","w")
        fin.write(string[:-1])
        fin.close()

    def add_positive_example(self,example, write_in_file=True):
        if(example in self.negative_example):
            self.negative_example.remove(example)

        if(example in self.positive_example):
            raise ValueError
        
        self.positive_example.append(example)

        if(write_in_file):
            self.write_in_file()


    def add_negative_example(self,example, write_in_file=True):

        if(example in self.positive_example):
            self.positive_example.remove(example)

        if(example in self.negative_example):
            raise ValueError



        self.negative_example.append(example)

        if(write_in_file):
            self.write_in_file()


class Explainer:

    def __init__(self, alphabet, traces="dummy.trace"):
        self.dfa=None
        self.ltl=None
        self.traces=traces
        self.alphabet=alphabet
        

    def learn_ltlf_and_dfa(self):
        learned_formulas = LTL_learner.learnLTL(self.traces)

        formulas=self._convert_formula(learned_formulas)

        self.ltl=formulas[0]

        self.dfa = DFA_learner.translate_ltl2dfa(alphabet=self.alphabet, formula=self.ltl)

        print("learned LTL formula:", self.ltl)
        # print(self.dfa)

    def _convert_formula(self, learned_formulas):
        # convert propositional variables in LTLf to human readable alphabet
        formulas=[]
        for formula in learned_formulas:
            formula=formula.prettyPrint()
            for idx in range(len(self.alphabet)):
                formula=formula.replace('x'+str(idx),self.alphabet[idx])
            formula=formula.replace("!","~")
            formulas.append(formula)
        return formulas


explainer=Explainer(alphabet=['a','b','c'])

    

    

    

