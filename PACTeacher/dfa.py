import string

import numpy as np
from IPython.display import Image
from IPython.display import display

import graphviz as gv
import functools

digraph = functools.partial(gv.Digraph, format='png')
graph = functools.partial(gv.Graph, format='png')
separator = "_"


class DFA:
    def __init__(self, init_state, final_states, transitions):
        self.final_states = final_states
        self.init_state = init_state
        self.transitions = transitions
        self.states = transitions.keys()
        self.alphabet = list(transitions[init_state].keys())
        self.current_state = self.init_state

    def is_word_in(self, w):
        s = self.init_state
        for l in w:
            s = self.transitions[s][l]
        return s in self.final_states

    def next_state_by_letter(self, s, l):
        q = self.transitions[s][l]
        return q

    def is_final_state(self, s):
        return s in self.final_states

    def is_word_letter_by_letter(self, letter, reset=False):
        if reset:
            self.current_state = self.init_state

        self.current_state = self.next_state_by_letter(self.current_state, letter)
        return self.current_state in self.final_states

    def reset_current_to_init(self):
        self.current_state = self.init_state

    def equivalence_with_counterexample(self, other):
        if self.is_word_in("") != other.is_word_in(""):
            return ""

        cross_states = {(self.init_state, other.init_state): ("", None)}
        to_check = [(self.init_state, other.init_state)]
        alphabet = self.alphabet

        while len(to_check) != 0:
            s1, s2 = to_check.pop(0)
            for l in alphabet:
                q1 = self.next_state_by_letter(s1, l)
                q2 = other.next_state_by_letter(s2, l)

                if (q1 in self.final_states) != (q2 in other.final_states):
                    counter_example = l
                    q1, q2 = s1, s2

                    while (q1 != self.init_state) | (q2 != other.init_state):
                        l, q1, q2 = cross_states.get((q1, q2))
                        counter_example = l + counter_example
                    return counter_example

                if cross_states.get((q1, q2)) is None:
                    to_check.append((q1, q2))
                    cross_states.update({(q1, q2): (l, s1, s2)})
        return None

    def __eq__(self, other):
        if self.is_word_in("") != other.is_word_in(""):
            return ""

        cross_states = {(self.init_state, other.init_state): ("", None)}
        to_check = [(self.init_state, other.init_state)]
        alphabet = self.alphabet

        while len(to_check) != 0:
            s1, s2 = to_check.pop(0)
            for l in alphabet:
                q1 = self.next_state_by_letter(s1, l)
                q2 = other.next_state_by_letter(s2, l)

                if (q1 in self.final_states) != (q2 in other.final_states):
                    return False

                if cross_states.get((q1, q2)) is None:
                    to_check.append((q1, q2))
                    cross_states.update({(q1, q2): (l, s1, s2)})
        return True

    def __repr__(self):
        return str(len(self.states)) + " states, " + str(len(self.final_states)) + " final states and " + \
               str(len(self.transitions)) + " transitions."

    # Stole the following function(draw_nicely) from lstar algo: https://github.com/tech-srl/lstar_extraction
    def draw_nicely(self, force=False, maximum=60,
                    name=""):  # todo: if two edges are identical except for letter, merge them
        # and note both the letters
        if (not force) and len(self.transitions) > maximum:
            return

        # suspicion: graphviz may be upset by certain sequences, avoid them in nodes
        label_to_number_dict = {False: 0}  # false is never a label but gets us started

        def label_to_numberlabel(label):
            max_number = max(label_to_number_dict[l] for l in label_to_number_dict)
            if not label in label_to_number_dict:
                label_to_number_dict[label] = max_number + 1
            return str(label_to_number_dict[label])

        def add_nodes(graph, nodes):  # stolen from http://matthiaseisen.com/articles/graphviz/
            for n in nodes:
                if isinstance(n, tuple):
                    graph.node(n[0], **n[1])
                else:
                    graph.node(n)
            return graph

        def add_edges(graph, edges):  # stolen from http://matthiaseisen.com/articles/graphviz/
            for e in edges:
                if isinstance(e[0], tuple):
                    graph.edge(*e[0], **e[1])
                else:
                    graph.edge(*e)
            return graph

        g = digraph()
        g = add_nodes(g, [(label_to_numberlabel(self.init_state),
                           {'color': 'green' if self.init_state in self.final_states else 'black',
                            'shape': 'hexagon', 'label': 'start'})])
        states = list(set(self.states) - {self.init_state})
        g = add_nodes(g, [(label_to_numberlabel(state), {'color': 'green' if state in self.final_states else 'black',
                                                         'label': str(i)})
                          for state, i in zip(states, range(1, len(states) + 1))])

        #
        # g = add_nodes(g, [(str(self.init_state),
        #                    {'color': 'green' if self.init_state in self.final_states else 'black',
        #                     'shape': 'hexagon', 'label': 'start'})])
        # states = list(set(self.states) - {self.init_state})
        # g = add_nodes(g, [(str(state), {'color': 'green' if state in self.final_states else 'black',
        #                                 'label': str(i)})
        #                   for state, i in zip(states, range(1, len(states) + 1))])

        def group_edges():
            def clean_line(line, group):
                line = line.split(separator)
                line = sorted(line) + ["END"]
                in_sequence = False
                last_a = ""
                clean = line[0]
                if line[0] in group:
                    in_sequence = True
                    first_a = line[0]
                    last_a = line[0]
                for a in line[1:]:
                    if in_sequence:
                        if a in group and (ord(a) - ord(last_a)) == 1:  # continue sequence
                            last_a = a
                        else:  # break sequence
                            # finish sequence that was
                            if (ord(last_a) - ord(first_a)) > 1:
                                clean += ("-" + last_a)
                            elif not last_a == first_a:
                                clean += (separator + last_a)
                            # else: last_a==first_a -- nothing to add
                            in_sequence = False
                            # check if there is a new one
                            if a in group:
                                first_a = a
                                last_a = a
                                in_sequence = True
                            if not a == "END":
                                clean += (separator + a)
                    else:
                        if a in group:  # start sequence
                            first_a = a
                            last_a = a
                            in_sequence = True
                        if not a == "END":
                            clean += (separator + a)
                return clean

            edges_dict = {}
            for state in self.states:
                for a in self.alphabet:
                    edge_tuple = (label_to_numberlabel(state), label_to_numberlabel(self.transitions[state][a]))
                    # print(str(edge_tuple)+"    "+a)
                    if not edge_tuple in edges_dict:
                        edges_dict[edge_tuple] = a
                    else:
                        edges_dict[edge_tuple] += separator + a
                    # print(str(edge_tuple)+"  =   "+str(edges_dict[edge_tuple]))
            for et in edges_dict:
                edges_dict[et] = clean_line(edges_dict[et], string.ascii_lowercase)
                edges_dict[et] = clean_line(edges_dict[et], string.ascii_uppercase)
                edges_dict[et] = clean_line(edges_dict[et], "0123456789")
                edges_dict[et] = edges_dict[et].replace(separator, ",")
            return edges_dict

        edges_dict = group_edges()
        g = add_edges(g, [(e, {'label': edges_dict[e]}) for e in edges_dict])
        # print('\n'.join([str(((str(state),str(self.delta[state][a])),{'label':a})) for a in self.alphabet for state in
        #                  self.Q]))
        # g = add_edges(g,[((label_to_numberlabel(state),label_to_numberlabel(self.delta[state][a])),{'label':a})
        #                  for a in self.alphabet for state in self.Q])
        # display(Image(filename=g.render(filename='img/automaton')))

        g.render(filename='img/automaton' + name)


def random_dfa(alphabet, min_states=10, max_states=100, min_final=1, max_final=10):
    states = np.random.randint(min_states, max_states)
    num_of_final = np.random.randint(min_final, max_final)
    initial_state = np.random.randint(1, states)

    final_states = np.random.choice(states, size=num_of_final, replace=False)

    transitions = {}
    for s in range(states):
        tran = {}
        for l in alphabet:
            q = np.random.randint(1, states)
            tran.update({l: q})
        transitions.update({s: tran})

    return DFA(initial_state, final_states.tolist(), transitions)

    # dfa = DFA(1, {1}, {1: {"a": 2, "b": 1, "c": 1},
    #                    2: {"a": 3, "b": 1, "c": 3},
    #                    3: {"a": 3, "b": 3, "c": 3}})

