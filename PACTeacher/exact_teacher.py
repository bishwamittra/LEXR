from PACTeacher.dfa import DFA
from PACTeacher.teacher import Teacher


class ExactTeacher(Teacher):

    def __init__(self, model: DFA):
        Teacher.__init__(self, model)

    def equivalence_query(self, dfa):
        return self.model.equivalence_with_counterexample(dfa)

    def membership_query(self, w):
        return self.model.is_word_in(w)

    def teach(self, learner):
        learner.teacher = self
        while True:
            counter = self.equivalence_query(learner.dfa)
            if counter is None:
                break
            learner.new_counterexample(counter)

