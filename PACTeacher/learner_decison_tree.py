import sys

from PACTeacher.dfa import DFA
from PACTeacher.learner import Learner


class TreeNode:
    def __init__(self, name="", inLan=True, parent=None):
        self.right = None
        self.left = None
        self.name = name
        self.inLan = inLan
        self.parent = parent

        if parent is not None:
            self.depth = parent.depth + 1
        else:
            self.depth = 0

    def __repr__(self):
        return "TreeNode: name: \'" + self.name + "\', depth:" + str(self.depth)


class DecisionTreeLearner(Learner):
    def __init__(self, teacher):
        self.teacher = teacher
        self._root = TreeNode(inLan=teacher.membership_query(""))
        self._leafs = [self._root]
        self.dfa = self._produce_hypothesis()

    def _sift(self, word):
        current_node = self._root
        while True:
            if current_node in self._leafs:
                return current_node

            if self.teacher.membership_query(word + current_node.name):
                current_node = current_node.right
            else:
                current_node = current_node.left

    def _produce_hypothesis(self):
        transitions = {}
        final_nodes = []
        for leaf in self._leafs:
            if leaf.inLan:
                final_nodes.append(leaf.name)
            tran = {}
            for l in self.teacher.alphabet:
                state = self._sift(leaf.name + l)
                tran.update({l: state.name})
            transitions.update({leaf.name: tran})

        return DFA("", final_nodes, transitions)

    def new_counterexample(self, w):
        first_time = False
        if len(self._leafs) == 1:
            new_differencing_string, new_state_string, first_time = self._leafs[0].name, w, True

        else:
            s = self.dfa.init_state
            prefix = ""
            for l in w:
                prefix = prefix + l
                n = self._sift(prefix)
                s = self.dfa.next_state_by_letter(s, l)
                if n.name != s:
                    for n2 in self._leafs:
                        if n2.name == s:
                            break
                    n = finding_common_ancestor(n, n2)
                    new_differencing_string = l + n.name
                    break

            new_state_string = prefix[0:len(prefix) - 1]

        node_to_replace = self._sift(new_state_string)
        # try:
        if self.teacher.membership_query(node_to_replace.name + new_differencing_string):
            node_to_replace.left = TreeNode(new_state_string, first_time^node_to_replace.inLan, node_to_replace)
            node_to_replace.right = TreeNode(node_to_replace.name, node_to_replace.inLan, node_to_replace)
        else:
            node_to_replace.right = TreeNode(new_state_string, first_time^node_to_replace.inLan, node_to_replace)
            node_to_replace.left = TreeNode(node_to_replace.name, node_to_replace.inLan, node_to_replace)
        # except :
        #     print(sys.exc_info()[0])
        self._leafs.remove(node_to_replace)
        node_to_replace.name = new_differencing_string
        self._leafs.extend([node_to_replace.right, node_to_replace.left])

        self.dfa = self._produce_hypothesis()
        # if self.dfa.is_word_in(prefix) != self._teacher.membership_query(prefix):
        #     print("?")


def finding_common_ancestor(node1: TreeNode, node2: TreeNode):
    if node1.depth < node2.depth:
        while node1.depth != node2.depth:
            node2 = node2.parent
    else:
        while node1.depth != node2.depth:
            node1 = node1.parent

    while node1 != node2:
        node1, node2 = node1.parent, node2.parent

    return node1
