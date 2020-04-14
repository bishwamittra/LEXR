from abc import ABC, abstractmethod

from PACTeacher.dfa import DFA


class Teacher(ABC):
    def __init__(self, model: DFA):
        """
        Constructor
        """
        self.model = model
        self.alphabet = model.alphabet

    @abstractmethod
    def membership_query(self, word):
        raise NotImplementedError()

    @abstractmethod
    def equivalence_query(self, dfa):
        raise NotImplementedError()
