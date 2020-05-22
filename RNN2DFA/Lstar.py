from RNN2DFA.ObservationTable import ObservationTable
import RNN2DFA.DFA as DFA
from time import clock
from multiprocessing import Process, Queue




def run_lstar(teacher, time_limit):
    table = ObservationTable(teacher.alphabet, teacher)
    start = clock()
    # teacher.counterexample_generator.set_time_limit(time_limit, start)
    # table.set_time_limit(time_limit, start)

    complete_before_timeout = False
    while True:
        while True:
            if(clock()-start > time_limit):
                print("Interrupted due to time limit")
                break
    
            while table.find_and_handle_inconsistency():
                if(clock()-start > time_limit):
                    print("Interrupted due to time limit")
                    break
            
                pass
            if table.find_and_close_row():
                continue
            else:
                break

        dfa = DFA.DFA(obs_table=table)

        counterexample = teacher.equivalence_query(dfa)
        if None is counterexample:
            complete_before_timeout = True
            break
        table.add_counterexample(
            counterexample, teacher.classify_word(counterexample))
        # check timeout
        if(clock()-start > time_limit):
            print("Interrupted due to time limit")
            break
    
    return dfa, complete_before_timeout
