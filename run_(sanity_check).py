

# %load_ext autoreload

# %autoreload 2

from RNN2DFA.LSTM import LSTMNetwork
# from GRU import GRUNetwork
from RNN2DFA.RNNClassifier import RNNClassifier
from RNN2DFA.Training_Functions import mixed_curriculum_train,make_train_set_for_target
import Tomita_Grammars 
from lstar_extraction.Training_Functions import make_test_set
from RNNexplainer import Explainer
import pandas as pd







benchmarks={
    "G(~a )":[
        "a",
        "~a",
        'F(a)',
        "F(~a)",
        "F(b)",
        "F(b|c)",
        "G(b|c)",
        'X(G(~a))',
        'X(G(a))'
    ]
    # ,
    # "G(b->X(~a))":[
    #     "true",
    #     "b",
    #     "X(b)", 
    #     "G(b)",
    #     "F(a)",
    #     "G(a)",
    # ]
    # ,
    # "G(b -> G(~a))":[
    #     "true",
    #     'G(b)',
    #     'G(~a)',
    #     'G(a)'
    # ],
    # "F(a)":[
    #     "true"
    # ],
    # "G(~a | F(a & F(b)))":[
    #     "true"
    # ],
    # "G(a & (~b -> (~b U(c & ~b)))) ":[
    #     "true"
    # ],
    # "G(a)":[
    #     "true"
    # ],
    # "F(b) -> (a U b)":[
    #     "true"
    # ],
    # "G(b -> G(a))":[
    #     "true"
    # ]

}


for target_formula in benchmarks:




    # make training set
    target = Tomita_Grammars.tomita_email
    alphabet = "abc"


    # use a dfa to generate training set
    fout=open("output/log.txt", "a")
    fout.write(".........................................................................\n")
    fout.write("Target: "+ target_formula)
    fout.write("\n")
    fout.close()
    import LTL2DFA as ltlf2dfa
    generator_dfa=ltlf2dfa.translate_ltl2dfa(alphabet=[character for character in alphabet],formula=target_formula)
    print(generator_dfa)


    # alphabet = "abcd"
    train_set = make_train_set_for_target(generator_dfa.classify_word,alphabet)
    print(train_set)

    # define rnn
    rnn = RNNClassifier(alphabet,num_layers=1,hidden_dim=10,RNNClass = LSTMNetwork)




    # train the model
    mixed_curriculum_train(rnn,train_set,stop_threshold = 0.0005)
    rnn.renew()  

    
    """  
    Igor's code:
    The model itself is implemented as a DFA. 
    """


    dfa_from_rnn=rnn 


    # use a query LTL formula
    import LTL2DFA as ltlf2dfa

    for query_formula in benchmarks[target_formula]:

        query_dfa=ltlf2dfa.translate_ltl2dfa(alphabet=[character for character in alphabet],formula=query_formula)
        # print(query_dfa)
        # query_dfa=No


        # make test_set supported by query dfa
        sample_test_set=make_train_set_for_target(query_dfa.classify_word, alphabet)

        # only consider sample that are true
        test_set=[]
        for key in sample_test_set:
            if(sample_test_set[key]):
                test_set.append(key)
        # print(test_set[:30])

        from PACTeacher.pac_teacher import PACTeacher as Teacher 

        # query_dfa=None

        if(query_dfa is None):
            query_formula=None
            test_set=make_test_set(alphabet)


        from RNNexplainer import Traces
        traces=Traces(rnn, alphabet)
        traces.label_from_network(test_set)
        traces.write_in_file()


        explainer=Explainer(alphabet=[character for character in alphabet])
        teacher = Teacher(dfa_from_rnn,epsilon=.001, delta=.001, max_trace_length=10, max_formula_depth=10, query_dfa=query_dfa)
        from time import clock
        start_time=clock()
        flag=teacher.teach(explainer,traces)
        end_time=clock()


        print("\n\nepsilon=", teacher.epsilon, "delta=", teacher.delta, "max_trace_length=", teacher.max_trace_length)
        print("query:", query_formula)
        print("final ltl: ", explainer.ltl)

        fout=open("output/log.txt", "a")
        fout.write("\n\nquery: "+query_formula)
        fout.write("\nfinal LTL: "+ explainer.ltl)
        if(not flag):
            fout.write(" [incomplete]")
            print("incomplete formula")
        fout.write("\n\n")

        print("\nTime taken:", end_time-start_time)

        fout.close()


        # statistics

        def percent(num,digits=2):
            tens = pow(10,digits)
            return int(100*num*tens)/tens

        test_set = train_set 
        print("testing on train set, i.e. test set is train set")
        # we're printing stats on the train set for now, but you can define other test sets by using
        # make_train_set_for_target

        n = len(test_set)
        print("test set size:", n)
        pos = len([w for w in test_set if generator_dfa.classify_word(w)])
        print("of which positive:",pos,"("+str(percent(pos/n))+")")
        rnn_target = len([w for w in test_set if rnn.classify_word(w)==generator_dfa.classify_word(w)])
        print("rnn score against target on test set:                             ",rnn_target,"("+str(percent(rnn_target/n))+")")

        fout=open("output/log.txt", "a")
        fout.write("rnn score against target on test set:                             "+str(rnn_target)+"("+str(percent(rnn_target/n))+")")
        fout.write("\n")

        performance_ltl = len([w for w in test_set if rnn.classify_word(w)==explainer.dfa.classify_word(w)])
        print("extracted LTL score against rnn on test set:                      ",performance_ltl,"("+str(percent(performance_ltl/n))+")")
        performance_ltl_with_target = len([w for w in test_set if explainer.dfa.classify_word(w)==generator_dfa.classify_word(w)])
        print("extracted LTL score against target on rnn's test set:             ",performance_ltl_with_target,"("+str(percent(performance_ltl_with_target/n))+")")

        performance_ltl = len([w for w in test_set if (rnn.classify_word(w)and query_dfa.classify_word(w)) ==explainer.dfa.classify_word(w)])
        print("extracted LTL score against rnn on test set (with query):         ",performance_ltl,"("+str(percent(performance_ltl/n))+")")
        fout.write("extracted LTL score against rnn on test set (with query):         "+str(performance_ltl)+"("+str(percent(performance_ltl/n))+")\n")
        performance_ltl_with_target = len([w for w in test_set if explainer.dfa.classify_word(w)== (generator_dfa.classify_word(w) and query_dfa.classify_word(w))])
        print("extracted LTL score against target on rnn's test set (with query):",performance_ltl_with_target,"("+str(percent(performance_ltl_with_target/n))+")")

        fout.write("extracted LTL score against target on rnn's test set (with query):"+str(performance_ltl_with_target)+"("+str(percent(performance_ltl_with_target/n))+")\n")
        fout.close()


        # report in a pandas file
        result = pd.DataFrame(columns=['target', 
                                        'query', 
                                        'explanation', 
                                        'status', 
                                        'rnn score', 
                                        'explanation score', 
                                        'explanation score on ground truth',
                                        'extraction time'
                                        ])

        result = result.append(
            {
                'target':target_formula,
                'query':query_formula,
                'explanation':explainer.ltl,
                'status':flag,
                'rnn score':percent(rnn_target/n),
                'explanation score':percent(performance_ltl/n),
                'explanation score on ground truth':percent(performance_ltl_with_target/n),
                'extraction time': end_time-start_time
            }, ignore_index=True
        )
        print(result.to_string(index=False))
        result.to_csv('output/result.csv', header=False, index=False, mode='a')


        # read result
        df=pd.read_csv("output/result.csv",header=None)
        df.columns=['target', 
                    'query', 
                    'explanation', 
                    'status', 
                    'rnn score', 
                    'explanation score', 
                    'explanation score on ground truth',
                    'extraction time'
                    ]
        print(df.to_string(index=False))

