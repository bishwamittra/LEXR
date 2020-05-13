from RNN2DFA.ObservationTable import ObservationTable
import RNN2DFA.DFA as DFA
from time import clock


def run_lstar(teacher, time_limit):
    table = ObservationTable(teacher.alphabet, teacher)
    start = clock()
    # teacher.counterexample_generator.set_time_limit(time_limit, start)
    table.set_time_limit(time_limit, start)

    complete_before_timeout = False
    while table.timed_out():
        while True:
            while table.find_and_handle_inconsistency():
                pass
            if table.find_and_close_row():
                continue
            else:
                break
        dfa = DFA.DFA(obs_table=table)
        # print("obs table refinement took " +
        #       str(int(1000*(clock()-start))/1000.0))
        print("\n")
        counterexample = teacher.equivalence_query(dfa)
        if None is counterexample:
            complete_before_timeout = False
            break
        start = clock()
        table.add_counterexample(
            counterexample, teacher.classify_word(counterexample))
    return dfa, complete_before_timeout
