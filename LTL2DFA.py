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


def translate_ltl2dfa(alphabet, formula=None, token=""):
    if(formula is None):
        formula = "F(a)"
    declare_flag = False  # True if you want to compute DECLARE assumption for the formula
    translator = Translator(formula, alphabet)
    translator.formula_parser()
    translator.translate()
    # it creates automa.mona file
    translator.createMonafile(declare_flag, path='./ltlf2dfa/automa'+token)
    # it returns an intermediate automa.dot file
    translator.invoke_mona(path='./ltlf2dfa/automa'+token)

    # print("\nLearning DFA from LTL")
    dfa = DFA()
    dfa.read_from_log(file='./ltlf2dfa/automa'+token+".log")
    # print(dfa)
    # print(dfa.classify_word('aaa'))

    dotHandler = DotHandler(path='./ltlf2dfa/automa'+token+'_inter.dot')
    dotHandler.modify_dot()
    # it returns the final automa.dot file
    dotHandler.output_dot(result_path='./ltlf2dfa/automa'+token)

    # dotHandler.extractDFA()

    return dfa


if __name__ == "__main__":
    # parseFormula()
    print(translate_ltl2dfa(alphabet=['a', 'b']))
