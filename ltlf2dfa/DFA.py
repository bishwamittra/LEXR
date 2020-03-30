

class DFA:
    def __init__(self):
        self.alphabet = []  # define alphabet
        self.Q = []  # set of states
        self.q0 = None  # initial states
        self.F = []  # final states
        self.delta = {}
        self.is_singleton_graph = False

    def read_from_log(self, file="./ltlf2dfa/automa.log"):
        fin = open(file, "r")
        lines = fin.readlines()
        for line in lines:
            if(line.startswith("DFA for formula with free variables: ")):
                line = line[:-1].strip()
                self.alphabet = line.split("DFA for formula with free variables: ", 1)[
                    1].lower().split(" ")
            elif(line.startswith("Initial state: ")):
                self.q0 = int(line.split("Initial state: ", 1)[1].strip())

            elif(line.startswith("Accepting states: ")):
                line = line.split("Accepting states: ", 1)[1][:-1].strip()
                if(" " in line):
                    print(line+".")
                    self.F = list(map(int, line.split(" ")))
                else:
                    self.F = [int(line)]
            elif(line.startswith("Automaton has ")):
                self.Q = [i for i in range(
                    int(line.split("Automaton has ", 1)[1].split(" ", 1)[0]))]

                if(len(self.Q) <= 2):
                    self.is_singleton_graph = True
                else:
                    # initial state is 1 when automata is not a singleto graph
                    self.q0 = 1
                    self.Q=self.Q[1:]

            elif(line.startswith("State ")):
                if(self.alphabet == []):
                    raise ValueError

                _, src, inputs, _, _, dest = line[:-1].strip().split(" ")
                src = int(src[:-1])
                dest = int(dest)
                # print(src, inputs, dest)
                if(src==0 and not self.is_singleton_graph):
                    continue

                if(src not in self.delta):
                    self.delta[src] = {}
                if('X' in inputs):
                    all_permutations=[""]
                    while(inputs):
                        # print(inputs)
                        temp=[]
                        for perm in all_permutations:
                            if(inputs[0]=='X'):
                                temp.append(perm+'0')
                                temp.append(perm+'1')
                            else:
                                temp.append(perm+inputs[0])
                        all_permutations=temp
                        inputs=inputs[1:]
                    # print(src, dest, all_permutations)
                    for perm in all_permutations:
                        self.delta[src][perm] = dest
                else:
                    self.delta[src][inputs] = dest

    #     self.modify_automata()

    # def modify_automata(self):
    #     if(not self.is_singleton_graph):
    #         del(self.delta[0])
    #     pass

    def classify_word(self, word):
        # simulate a run and then look at the reached state. If the reached state is in the set of final states, then classify positive
        # else classify negative. 

        word=word.lower()
        q=self.q0
        while(word):
            
            transition_input=""
            for symbol in self.alphabet:
                if(symbol==word[0]):
                    transition_input+='1'
                else:
                    transition_input+='0'
            word=word[1:]
            
            # make transition
            q=self.delta[q][transition_input]
            
        if(q in self.F):
            return True
        return False

    def __repr__(self):
        return "DFA:->\n"+'\n'.join(" - %s: %s" % (item, value) for (item, value) in vars(self).items() if "__" not in item)
