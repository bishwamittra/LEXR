from time import clock
from RNN2DFA.ObservationTable import TableTimedOut
from RNN2DFA.DFA import DFA
from RNN2DFA.Teacher import Teacher
from RNN2DFA.Lstar import run_lstar


def extract(rnn, query = None , max_trace_length=20, epsilon=.05, delta=.05, time_limit=50, initial_split_depth=10, starting_examples=None):
    print("provided counterexamples are:", starting_examples)
    guided_teacher = Teacher(
        rnn, query, num_dims_initial_split=initial_split_depth, starting_examples=starting_examples, epsilon=epsilon, delta = delta, max_trace_length=max_trace_length)

    start = clock()
    try:
        _, flag =run_lstar(guided_teacher, time_limit)
    except KeyboardInterrupt:  # you can press the stop button in the notebook to stop the extraction any time
        print("lstar extraction terminated by user")
    except TableTimedOut:
        print("observation table timed out during refinement")
    end = clock()
    extraction_time = end-start

    dfa = guided_teacher.dfas[-1]

    print("overall guided extraction time took: " + str(extraction_time))

    print("generated counterexamples were: (format: (counterexample, counterexample generation time))")
    print('\n'.join([str(a)
                     for a in guided_teacher.counterexamples_with_times]))
    return dfa, flag
