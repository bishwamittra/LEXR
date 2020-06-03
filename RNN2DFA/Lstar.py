from RNN2DFA.ObservationTable import ObservationTable
import RNN2DFA.DFA as DFA
from time import clock
from multiprocessing import Process, Queue




def run_lstar(teacher, time_limit):
    table = ObservationTable(teacher.alphabet, teacher)
    start = clock()
    # teacher.counterexample_generator.set_time_limit(time_limit, start)
    # table.set_time_limit(time_limit, start)

    complete_before_timeout = True
    while True:
        while True:
            if(clock()-start > time_limit):
                print("1 Interrupted due to time limit")
                complete_before_timeout = False
                break
    
            while table.find_and_handle_inconsistency():
                if(clock()-start > time_limit):
                    print("2 Interrupted due to time limit")
                    complete_before_timeout = False
                    break
            
                pass
            if table.find_and_close_row():
                continue
            else:
                break
        
        if(not complete_before_timeout):
            break

        dfa = DFA.DFA(obs_table=table)

        counterexample = teacher.equivalence_query(dfa)
        if None is counterexample:
            break
        table.add_counterexample(
            counterexample, teacher.classify_word(counterexample))
        # check timeout
        if(clock()-start > time_limit):
            print("3 Interrupted due to time limit")
            complete_before_timeout = False
            break
    
    return dfa, complete_before_timeout
