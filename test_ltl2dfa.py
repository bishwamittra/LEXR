import os
import sys
from ltlf2dfa.Parser import MyParser
from ltlf2dfa.Translator import Translator
from ltlf2dfa.DotHandler import DotHandler
from ltlf2dfa.DFA import DFA


def parseFormula():
    formula = "G(a->Xb)"
    parser = MyParser()
    parsed_formula = parser(formula)
    print(parsed_formula)


def translate_ltl2dfa():
    formula = "F(aUb)"
    declare_flag = False  # True if you want to compute DECLARE assumption for the formula
    translator = Translator(formula)
    translator.formula_parser()
    translator.translate()
    translator.createMonafile(declare_flag)  # it creates automa.mona file
    translator.invoke_mona()  # it returns an intermediate automa.dot file

    dfa = DFA()
    dfa.read_from_log()
    print(dfa)
    print(dfa.classify_word('aaa'))

    dotHandler = DotHandler()
    dotHandler.modify_dot()
    dotHandler.output_dot() #it returns the final automa.dot file

    # clean
    # os.system("./clean.sh")

    # dotHandler.extractDFA()


if __name__ == "__main__":
    # parseFormula()
    translate_ltl2dfa()
