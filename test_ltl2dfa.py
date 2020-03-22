from ltlf2dfa.Parser import MyParser
from ltlf2dfa.Translator import Translator
from ltlf2dfa.DotHandler import DotHandler


def parseFormula():
    formula = "G(a->Xb)"
    parser = MyParser()
    parsed_formula = parser(formula)
    print(parsed_formula)

def translate_ltl2dfa():
    formula = "G(a->Xb)"
    declare_flag = False #True if you want to compute DECLARE assumption for the formula
    translator = Translator(formula)
    translator.formula_parser()
    translator.translate()
    translator.createMonafile(declare_flag) #it creates automa.mona file
    translator.invoke_mona() #it returns an intermediate automa.dot file
    dotHandler = DotHandler()
    dotHandler.modify_dot()
    dotHandler.output_dot() #it returns the final automa.dot file
    
if __name__ == "__main__":
    # parseFormula()
    translate_ltl2dfa()
