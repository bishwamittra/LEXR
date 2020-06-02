import pandas as pd
import numpy as np
pd.options.display.max_colwidth = 400
pd.options.mode.chained_assignment = None  # default='warn'


df = pd.read_csv("output/result.csv", header=None)
df.columns = ['target',
              'query',
              'explanation',
              'status',
              'test accuracy',
              'rnn score',
              'explanation score',
              'explanation score on ground truth',
              'extraction time',
              'revised delta',
              'revised epsilon',
              'counterexamples',
              'train size',
              'test size',
              'ltl_depth',
            'lstar states',
            'lstar explanation score',
            'lstar explanation score on ground truth',
            'lstar extraction time',
            'lstar status', 
            'epsilon', 
            'delta'
              ]


df = df[(df['explanation score']!=0) & (df['lstar explanation score']!=0)]



print("\n\n\n\n\n\n")
print("""  
   \\begin{table}
   \\scriptsize
      \\begin{center}
         \\begin{tabular}{lp{4cm}p{4cm}rrrrr}
            \\toprule
            & Query & \\multicolumn{3}{c}{LTL} & \\multicolumn{3}{c}{DFA} \\\\
            \\cmidrule(r){3-5}
            \\cmidrule(r){6-8}	
            & & Explanation & Acc &  Time & |Q| & Acc &  Time\\\\
            \\midrule
""")



# read email_match
email_df = df[(df['target'] == "email match") 
            & (df['query'] != "false")
            & (df['epsilon'] == 0.05) 
            &  (df['delta'] == 0.05)][[
    'query', 'explanation', 'ltl_depth', 'explanation score', 'extraction time', 'lstar states', 'lstar explanation score', 'lstar extraction time']]
replace_dict = dict(zip([
    "X",
    '\|',
    "U",
    "F",
    "G",
    "d",
    "&",
    "~",
    "false",
    "a",
    "->",
    "true",
], [
    "\\\\X ",
    "\\\\vee ",
    "\\\\U ",
    "\\\\F ",
    "\\\\G ",
    "\\\\circ ",
    " \\\\wedge ",
    " \\\\neg ",
    "\\\\bot",
    "@",
    " \\\\rightarrow",
    "\\\\top",
]))
email_df['query'] = '& $ ' + email_df['query'].str.strip().replace(replace_dict,
                                                                 regex=True) + ' $  &'
                                                            

# remove parenthesis in starting and end of explanation
email_df['explanation'] = email_df['explanation'].apply(lambda x: x[1:-1] if (x[0]=="(" and x[-1] == ")") else x)
email_df.loc[email_df['extraction time'] > 400, 'extraction time'] = 400
email_df.loc[email_df['lstar extraction time'] > 400, 'lstar extraction time'] = 400

email_df['explanation'] = '$ ' + \
    email_df['explanation'].str.strip().replace(
        replace_dict, regex=True) + ' $  &'
email_df['ltl_depth'] = '$ ' + \
        email_df['ltl_depth'].round(2).astype(str) + ' $  &'
         
# email_df['status'] = email_df['status'].astype(str) + ' &'
mask = pd.to_numeric(email_df['explanation score']).notnull()
# email_df['explanation score'].loc[mask] = email_df['explanation score'].loc[mask].astype(np.int64)

email_df['explanation score'] = '$ ' + \
    email_df['explanation score'].round(2).astype(str) + ' $  &'
email_df['extraction time'] = '$ ' + \
    email_df['extraction time'].round(2).astype(str) + ' $  &'
mask = pd.to_numeric(email_df['lstar explanation score']).notnull()
# email_df['lstar explanation score'].loc[mask] = email_df['lstar explanation score'].loc[mask].astype(np.int64)
email_df['lstar states'] = '$ ' + \
    email_df['lstar states'].round(2).astype(str) + ' $ &'

email_df['lstar explanation score'] = '$ ' + \
    email_df['lstar explanation score'].round(2).astype(str) + ' $  &'
email_df['lstar extraction time'] = '$ ' + \
    email_df['lstar extraction time'].round(2).astype(str) + ' $  \\\\'

pd.options.display.max_colwidth = 400




print("\\parbox[t]{2mm}{\\multirow{"+str(len(email_df.index))+"}{*}{\\rotatebox[origin=c]{90}{Email Match}}}")
print(email_df[['query', 'explanation',   'explanation score',
                    'extraction time', 'lstar states', 'lstar explanation score',
                    'lstar extraction time']].to_string(index=False,  header=None))
print("       \\midrule\n\n\n\n\n")












bp_df = df[(df['target'] == "balanced parentheses") 
        & (df['query'] != "false")
        & (df['epsilon'] == 0.05) 
        &  (df['delta'] == 0.05)][[
    'query', 'explanation', 'ltl_depth', 'explanation score', 'extraction time', 'lstar states', 'lstar explanation score', 'lstar extraction time']]

replace_dict = dict(zip([
    #    "d",
    "X",
    '\|',
    "U",
    "F",
    "G",
    "&",
    "~",
    "->",
    "true",
    "false",
    #    "a"
], [

    #    "\\\\circ",
    "\\\\X ",
    "\\\\vee ",
    "\\\\U ",
    "\\\\F ",
    "\\\\G ",
    " \\\\wedge ",
    " \\\\neg ",
    " \\\\rightarrow",
    "\\\\top",
    "\\\\bot",
    #    "@"
]))
bp_df['query'] = '& $ ' + bp_df['query'].str.strip().replace(replace_dict,
                                                           regex=True) + ' $  &'
# remove parenthesis in starting and end of explanation
bp_df['explanation'] = bp_df['explanation'].apply(lambda x: x[1:-1] if (x[0]=="(" and x[-1] == ")") else x)
bp_df.loc[bp_df['extraction time'] > 400, 'extraction time'] = 400
bp_df.loc[bp_df['lstar extraction time'] > 400, 'lstar extraction time'] = 400

bp_df['explanation'] = '$ ' + \
    bp_df['explanation'].str.strip().replace(replace_dict, regex=True) + ' $ &'
bp_df['ltl_depth'] = '$ ' + \
        bp_df['ltl_depth'].round(2).astype(str) + ' $  &'
           
# bp_df['status'] = bp_df['status'].astype(str) + ' &'
mask = pd.to_numeric(bp_df['explanation score']).notnull()
# bp_df['explanation score'].loc[mask] = bp_df['explanation score'].loc[mask].astype(np.int64)

bp_df['explanation score'] = '$ ' + \
    bp_df['explanation score'].round(2).astype(str) + ' $  &'
bp_df['extraction time'] = '$ ' + \
    bp_df['extraction time'].round(2).astype(str) + ' $ &'
mask = pd.to_numeric(bp_df['lstar explanation score']).notnull()
# bp_df['lstar explanation score'].loc[mask] = bp_df['lstar explanation score'].loc[mask].astype(np.int64)
bp_df['lstar states'] = '$ ' + \
    bp_df['lstar states'].round(2).astype(str) + ' $ &'

bp_df['lstar explanation score'] = '$ ' + \
    bp_df['lstar explanation score'].round(2).astype(str) + ' $  &'
bp_df['lstar extraction time'] = '$ ' + \
    bp_df['lstar extraction time'].round(2).astype(str) + ' $  \\\\'

pd.options.display.max_colwidth = 400




print("\\parbox[t]{2mm}{\\multirow{"+str(len(bp_df.index))+"}{*}{\\rotatebox[origin=c]{90}{Balanced Parentheses}}}")
print(bp_df[['query', 'explanation',   'explanation score',
                    'extraction time', 'lstar states', 'lstar explanation score',
                    'lstar extraction time']].to_string(index=False,  header=None))
print("       \\midrule\n\n\n\n\n")









abp_df = df[(df['target'] == "alternating bit protocol") 
            &  (df['query'] != "false")
            & (df['epsilon'] == 0.05) 
            &  (df['delta'] == 0.05)][[
    'query', 'explanation', 'ltl_depth','explanation score', 'extraction time', 'lstar states', 'lstar explanation score', 'lstar extraction time']]
replace_dict = dict(zip([
    #    "d",
    "b",
    "X",
    '\|',
    "U",
    "F",
    "G",
    "~",
    "true",
    "false",
    "a",
    "->",
    "c",
    "d",
    "&",

], [

    #    "\\\\circ",
    "\\\\text{msg}1",
    "\\\\X ",
    "\\\\vee ",
    "\\\\U ",
    "\\\\F ",
    "\\\\G ",
    " \\\\neg ",
    "\\\\top",
    "\\\\bot",
    "\\\\text{msg}0",
    " \\\\rightarrow",
    "\\\\text{ack}0",
    "\\\\text{ack}1",
    " \\\\wedge ",

    #    "@"
]))
abp_df['query'] = '& $ ' + abp_df['query'].str.strip().replace(replace_dict,
                                                             regex=True) + ' $  &'
# remove parenthesis in starting and end of explanation
abp_df['explanation'] = abp_df['explanation'].apply(lambda x: x[1:-1] if (x[0]=="(" and x[-1] == ")") else x)
abp_df.loc[abp_df['extraction time'] > 400, 'extraction time'] = 400
abp_df.loc[abp_df['lstar extraction time'] > 400, 'lstar extraction time'] = 400


abp_df['explanation'] = '$ ' + \
    abp_df['explanation'].str.strip().replace(
        replace_dict, regex=True) + ' $ &'
abp_df['ltl_depth'] = '$ ' + \
        abp_df['ltl_depth'].round(2).astype(str) + ' $  &'
        
    
# abp_df['status'] = abp_df['status'].astype(str) + ' &'
mask = pd.to_numeric(abp_df['explanation score']).notnull()
# abp_df['explanation score'].loc[mask] = abp_df['explanation score'].loc[mask].astype(np.int64)

abp_df['explanation score'] = '$ ' + \
    abp_df['explanation score'].round(2).astype(str) + ' $  &'
abp_df['extraction time'] = '$ ' + \
    abp_df['extraction time'].round(2).astype(str) + ' $  &'
mask = pd.to_numeric(abp_df['lstar explanation score']).notnull()
# abp_df['lstar explanation score'].loc[mask] = abp_df['lstar explanation score'].loc[mask].astype(np.int64)
abp_df['lstar states'] = '$ ' + \
    abp_df['lstar states'].round(2).astype(str) + ' $ &'

abp_df['lstar explanation score'] = '$ ' + \
    abp_df['lstar explanation score'].round(2).astype(str) + ' $  &'
abp_df['lstar extraction time'] = '$ ' + \
    abp_df['lstar extraction time'].round(2).astype(str) + ' $  \\\\'

pd.options.display.max_colwidth = 400






print("\\parbox[t]{2mm}{\\multirow{"+str(len(abp_df.index) + 6)+"}{*}{\\rotatebox[origin=c]{90}{Alternate Bit Protocol}}}")
print(abp_df[['query', 'explanation',   'explanation score',
                    'extraction time', 'lstar states', 'lstar explanation score',
                    'lstar extraction time']].to_string(index=False,  header=None))


print("\n\n\n")

print(""" 
        \\bottomrule
        \\end{tabular}
    \\end{center} """)

print("      \\caption{Explanation on practical problems.}")
print("      \\label{tab:example-practical}")
print("\\end{table} ")














if(True):

    # unified:
    print("\n\n\n\n\n\n")
    print("""  
    \\begin{table}
        \\begin{center}
            \\begin{tabular}{lp{2cm}p{3cm}rrrrr}
                \\toprule
                Language & Query & \\multicolumn{3}{c}{LTL} & \\multicolumn{3}{c}{DFA} \\\\
                \\cmidrule(r){3-5}
                \\cmidrule(r){6-8}	
                & & Explanation & Acc &  Time & |Q| & Acc &  Time\\\\
                \\midrule
    """)


    # for the other examples
    other_examples_df = df[(df['target'] != "email match") &
                        (df['target'] != "alternating bit protocol") &
                        (df['target'] != "balanced parentheses") & 
                        (df['target'] != "F(aUb)") & 
                        #    (df['query'] != "false") &
                        (df['epsilon'] == 0.05) &
                        (df['delta'] == 0.05)]

    cnt = 0
    for formula, each_df in other_examples_df.groupby(['target']):

        replace_dict = dict(zip([
            #    "d",
            "X",
            '\|',
            "U",
            "F",
            "G",
            "&",
            "~",
            "->",
            "true",
            "false",
        ], [

            #    "\\\\circ",
            "\\X ",
            "\\vee ",
            "\\U ",
            "\\F ",
            "\\G ",
            " \\wedge ",
            " \\neg ",
            " \\rightarrow",
            "\\top",
            "\\bot",
        ]))

        for key in replace_dict.keys():
            formula = formula.replace(key, replace_dict[key])

        print(" $ " + formula +" $ ")

        replace_dict = dict(zip([
            #    "d",
            "X",
            '\|',
            "U",
            "F",
            "G",
            "&",
            "~",
            "->",
            "true",
            "false",
        ], [

            #    "\\\\circ",
            "\\\\X ",
            "\\\\vee ",
            "\\\\U ",
            "\\\\F ",
            "\\\\G ",
            " \\\\wedge ",
            " \\\\neg ",
            " \\\\rightarrow",
            "\\\\top",
            "\\\\bot",
        ]))

        each_df['query'] = '& $ ' + each_df['query'].str.strip().replace(replace_dict,
                                                                    regex=True) + ' $  &'

        # remove parenthesis in starting and end of explanation
        each_df['explanation'] = each_df['explanation'].apply(lambda x: x[1:-1] if (x[0]=="(" and x[-1] == ")") else x)
        
        each_df['explanation'] = '$ ' + \
            each_df['explanation'].str.strip().replace(
            replace_dict, regex=True) + ' $ &'
        # each_df['status'] = each_df['status'].astype(str) + ' &'
    #  each_df['explanation score'] = each_df['explanation score'].apply(lambda x : '{0:,}'.format(x))
        
        each_df.loc[each_df['extraction time'] > 400, 'extraction time'] = 400
        each_df.loc[each_df['lstar extraction time'] > 400, 'lstar extraction time'] = 400
        mask = pd.to_numeric(each_df['explanation score']).notnull()
        # each_df['explanation score'].loc[mask] = each_df['explanation score'].loc[mask].astype(np.int64)
        each_df['explanation score'] = '$ ' + \
            each_df['explanation score'].round(2).astype(str) + ' $  &'
        each_df['extraction time'] = '$ ' + \
            each_df['extraction time'].round(2).astype(str) + ' $  &'
        each_df['ltl_depth'] = '$ ' + \
            each_df['ltl_depth'].round(2).astype(str) + ' $  &'
        
        mask = pd.to_numeric(each_df['lstar explanation score']).notnull()
        # each_df['lstar explanation score'].loc[mask] = each_df['lstar explanation score'].loc[mask].astype(np.int64)
        each_df['lstar states'] = '$ ' + \
            each_df['lstar states'].round(2).astype(str) + ' $ &'

        each_df['lstar explanation score'] = '$ ' + \
            each_df['lstar explanation score'].round(2).astype(str) + ' $  &'
        each_df['lstar extraction time'] = '$ ' + \
            each_df['lstar extraction time'].round(2).astype(str) + ' $  \\\\'

        
        
        

        print(each_df[['query', 'explanation',   'explanation score',
                    'extraction time', 'lstar states', 'lstar explanation score',
                    'lstar extraction time']].to_string(index=False, header=None))
        print("       \\midrule\n")
    print("\n\n\n")

    print(""" 
            \\bottomrule
            \\end{tabular}
        \\end{center} """)

    print("      \\caption{Explanation of synthetic problems.}")
    print("      \\label{tab:example-synthetic}")
    print("\\end{table} ")





