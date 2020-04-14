from PACTeacher.teacher import Teacher
from tulip.transys import automata
from abc import ABC, abstractmethod


class Learner(ABC):

    def __init__(self, teacher: Teacher):
        """
        constructor
        """
        self.teacher = teacher

    @abstractmethod
    def new_counterexample(self):
        pass
