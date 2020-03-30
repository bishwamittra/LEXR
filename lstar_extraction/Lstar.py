from lstar_extraction.ObservationTable import ObservationTable
import lstar_extraction.DFA as DFA
from time import clock

def run_lstar(teacher,time_limit):
    print('\ndo we come to this point?')
    table = ObservationTable(teacher.alphabet,teacher)
    start = clock()
    teacher.counterexample_generator.set_time_limit(time_limit,start)
    table.set_time_limit(time_limit,start)
    while True:
        print("\ndon't know how many times it is visited")
        while True:
            while table.find_and_handle_inconsistency():
                pass
            if table.find_and_close_row():
                continue
            else:
                break
        dfa = DFA.DFA(obs_table=table)
        
        print("obs table refinement took " + str(int(1000*(clock()-start))/1000.0) )
        counterexample = teacher.equivalence_query(dfa)
        print("DFA:", dfa)
        print("counter examples:", counterexample)
        if None is counterexample:
            break
        start = clock()
        table.add_counterexample(counterexample,teacher.classify_word(counterexample))
    return dfa