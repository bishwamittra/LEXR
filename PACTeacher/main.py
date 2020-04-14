from copy import deepcopy

from tulip.transys import automata

from dfa import DFA, random_dfa
from exact_teacher import ExactTeacher
from lstar.LSTM import LSTMNetwork
from learner_decison_tree import DecisionTreeLearner
from lstar.RNNClassifier import RNNClassifier
from lstar.Training_Functions import make_train_set_for_target, mixed_curriculum_train
from pac_teacher import PACTeacher

if __name__ == '__main__':
    pass


def target(w):
    if("a" in w ):
        return True
    return False


dfa_rand = random_dfa(["a", "b"], min_states=10, max_states=20, min_final=1,
                      max_final=3)
dfa_rand.draw_nicely(name="_rand")

target = dfa_rand.is_word_in

alphabet = "ab"

train_set = make_train_set_for_target(target, alphabet)
rnn = RNNClassifier(alphabet, num_layers=2, hidden_dim=10, RNNClass=LSTMNetwork)
mixed_curriculum_train(rnn, train_set, stop_threshold=0.0005)

print("done learning")

while True:
    # try:
    teacher_pac = PACTeacher(rnn)
    student_pac = DecisionTreeLearner(teacher_pac)
    teacher_pac.teach(student_pac)
    print("dfa learned")
    student_pac.dfa.draw_nicely(name="rnn")
    break
    # except:
    print("Asd")

if student_pac.dfa == dfa_rand:
    print("cool")
else:
    print("oh well")
