# from lstar_extraction.ObservationTable import ObservationTable
from test_xRNN import Explainer
# import lstar_extraction.DFA as DFA
from time import clock

def run_lstar(teacher,time_limit, alphabet, traces):
    # table = ObservationTable(teacher.alphabet,teacher)
    start = clock()
    explainer=Explainer(alphabet=[character for character in alphabet])
    teacher.counterexample_generator.set_time_limit(time_limit,start)
    # table.set_time_limit(time_limit,start)
    while True:
        print("\n\n")
        # print("\ndon't know how many times it is visited")
        # while True:
        #     while table.find_and_handle_inconsistency():
        #         pass
        #     if table.find_and_close_row():
        #         continue
        #     else:
        #         break
        # dfa = DFA.DFA(obs_table=table)
        
        explainer.learn_ltlf_and_dfa()
        dfa=explainer.dfa
        print("obs table refinement took " + str(int(1000*(clock()-start))/1000.0) )
        counterexample = teacher.equivalence_query(dfa,explainer.ltl)
        
        
        if None is counterexample:
            break
        start = clock()
        
        # table.add_counterexample(counterexample,teacher.classify_word(counterexample))
        
        '''
        implement method that can add counterexamples and learn again. 
        
        '''

        # print("counter examples:", counterexample)
        # print("prediction of counter-example: (dfa)", dfa.classify_word(counterexample))
        # print("prediction of counter-example: (rnn)", teacher.network.classify_word(counterexample))
        # print(traces)
        # print(dfa)

        if(dfa.classify_word(counterexample)):
            traces.add_negative_example(counterexample)
        else:
            traces.add_positive_example(counterexample)

        # break

    return dfa