import pandas as pd
import numpy as np
pd.options.display.max_colwidth = 400
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


# read email_match
email_df = df[(df['target'] == "email match") & (df['query'] != "false")][[
    'query', 'explanation', 'explanation score', 'extraction time', 'lstar states', 'lstar explanation score', 'lstar extraction time']]
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
email_df['query'] = '$ ' + email_df['query'].str.strip().replace(replace_dict,
                                                                 regex=True) + ' $  &'
email_df['explanation'] = '$ ' + \
    email_df['explanation'].str.strip().replace(
        replace_dict, regex=True) + ' $  &'
# email_df['status'] = email_df['status'].astype(str) + ' &'
mask = pd.to_numeric(email_df['explanation score']).notnull()
email_df['explanation score'].loc[mask] = email_df['explanation score'].loc[mask].astype(np.int64)

email_df['explanation score'] = '$ ' + \
    email_df['explanation score'].round(2).astype(str) + ' $  &'
email_df['extraction time'] = '$ ' + \
    email_df['extraction time'].round(2).astype(str) + ' $  &'
mask = pd.to_numeric(email_df['lstar explanation score']).notnull()
email_df['lstar explanation score'].loc[mask] = email_df['lstar explanation score'].loc[mask].astype(np.int64)
email_df['lstar states'] = '$ ' + \
    email_df['lstar states'].round(2).astype(str) + ' $ &'

email_df['lstar explanation score'] = '$ ' + \
    email_df['lstar explanation score'].round(2).astype(str) + ' $  &'
email_df['lstar extraction time'] = '$ ' + \
    email_df['lstar extraction time'].round(2).astype(str) + ' $  \\\\'

pd.options.display.max_colwidth = 400


print("""  
   \\begin{table}
      \\begin{center}
         \\begin{tabular}{llrr@{\\hskip 0.4in}rrr}
            \\toprule
            Query& \\multicolumn{3}{c}{LTL} & \\multicolumn{3}{c}{DFA} \\\\
			& Explanation  & Acc(\%) &  Time(s) & |Q| & Acc(\%) &  Time(s)\\\\
            \\midrule
   """)


print(email_df.to_string(index=False,  header=None))

print(""" 
            \\bottomrule
         \\end{tabular}
      \\end{center} """)
print("      \\caption{Explanation for email match ([a-z][a-z0-9]*@[a-z0-9]+.com\\$). Here $ \\{p,q,r\\} $ replaces the set $ [a-z] $, $ \\{m,n\\} $ replaces the set $ [0-9] $, $ \\circ $ replaces  `.'  (dot)}")
print("      \\label{tab:example-email}")
print("\\end{table} ")

print("\n\n")











bp_df = df[(df['target'] == "balanced parentheses") & (df['query'] != "false")][[
    'query', 'explanation', 'explanation score', 'extraction time', 'lstar states', 'lstar explanation score', 'lstar extraction time']]

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
bp_df['query'] = '$ ' + bp_df['query'].str.strip().replace(replace_dict,
                                                           regex=True) + ' $  &'
bp_df['explanation'] = '$ ' + \
    bp_df['explanation'].str.strip().replace(replace_dict, regex=True) + ' $ &'
# bp_df['status'] = bp_df['status'].astype(str) + ' &'
mask = pd.to_numeric(bp_df['explanation score']).notnull()
bp_df['explanation score'].loc[mask] = bp_df['explanation score'].loc[mask].astype(np.int64)

bp_df['explanation score'] = '$ ' + \
    bp_df['explanation score'].round(2).astype(str) + ' $  &'
bp_df['extraction time'] = '$ ' + \
    bp_df['extraction time'].round(2).astype(str) + ' $ &'
mask = pd.to_numeric(bp_df['lstar explanation score']).notnull()
bp_df['lstar explanation score'].loc[mask] = bp_df['lstar explanation score'].loc[mask].astype(np.int64)
bp_df['lstar states'] = '$ ' + \
    bp_df['lstar states'].round(2).astype(str) + ' $ &'

bp_df['lstar explanation score'] = '$ ' + \
    bp_df['lstar explanation score'].round(2).astype(str) + ' $  &'
bp_df['lstar extraction time'] = '$ ' + \
    bp_df['lstar extraction time'].round(2).astype(str) + ' $  \\\\'

pd.options.display.max_colwidth = 400


print("""  
   \\begin{table}
      \\begin{center}
         \\begin{tabular}{llrr@{\\hskip 0.4in}rrr}
            \\toprule
            Query& \\multicolumn{3}{c}{LTL} & \\multicolumn{3}{c}{DFA} \\\\
			& Explanation  & Acc(\%) &  Time(s) & |Q| & Acc(\%) &  Time(s)\\\\
            \\midrule
   """)


print(bp_df.to_string(index=False,  header=None))

print(""" 
            \\bottomrule
         \\end{tabular}
      \\end{center} """)
print("      \\caption{Explanation for balanced parenthesis where symbol $ l $ replaces the left parenthesis `(' and symbol $ r $ replaces the right parenthesis `)'.}")
print("      \\label{tab:example-bp}")
print("\\end{table} ")

print("\n\n")









abp_df = df[(df['target'] == "alternating bit protocol") &  (df['query'] != "false")][[
    'query', 'explanation', 'explanation score', 'extraction time', 'lstar states', 'lstar explanation score', 'lstar extraction time']]
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
abp_df['query'] = '$ ' + abp_df['query'].str.strip().replace(replace_dict,
                                                             regex=True) + ' $  &'
abp_df['explanation'] = '$ ' + \
    abp_df['explanation'].str.strip().replace(
        replace_dict, regex=True) + ' $ &'
# abp_df['status'] = abp_df['status'].astype(str) + ' &'
mask = pd.to_numeric(abp_df['explanation score']).notnull()
abp_df['explanation score'].loc[mask] = abp_df['explanation score'].loc[mask].astype(np.int64)

abp_df['explanation score'] = '$ ' + \
    abp_df['explanation score'].round(2).astype(str) + ' $  &'
abp_df['extraction time'] = '$ ' + \
    abp_df['extraction time'].round(2).astype(str) + ' $  &'
mask = pd.to_numeric(abp_df['lstar explanation score']).notnull()
abp_df['lstar explanation score'].loc[mask] = abp_df['lstar explanation score'].loc[mask].astype(np.int64)
abp_df['lstar states'] = '$ ' + \
    abp_df['lstar states'].round(2).astype(str) + ' $ &'

abp_df['lstar explanation score'] = '$ ' + \
    abp_df['lstar explanation score'].round(2).astype(str) + ' $  &'
abp_df['lstar extraction time'] = '$ ' + \
    abp_df['lstar extraction time'].round(2).astype(str) + ' $  \\\\ \\rule{0pt}{3ex}'

pd.options.display.max_colwidth = 400




print("""  
   \\begin{table}
      \\begin{center}
         \\begin{tabular}{p{5 cm}@{\\hskip 0.2in}p{5 cm}rr@{\\hskip 0.4in}rrr}
            \\toprule
            Query& \\multicolumn{3}{c}{LTL} & \\multicolumn{3}{c}{DFA} \\\\
			& Explanation  & Acc(\%) &  Time(s) & |Q| & Acc(\%) &  Time(s)\\\\
            \\midrule
   """)


print(abp_df.to_string(index=False,  header=None))

print(""" 
            \\bottomrule
         \\end{tabular}
      \\end{center} """)
print("      \\caption{Explanation for alternating bit protocol in Figure~\\ref{fig:alternating-bit-protocol}.}")
print("      \\label{tab:example-abp}")
print("\\end{table} ")

print("\n\n")












# for the other examples
other_examples_df = df[(df['target'] != "email match") &
                       (df['target'] != "alternating bit protocol") &
                       (df['target'] != "balanced parentheses") & 
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
    each_df['query'] = '$ ' + each_df['query'].str.strip().replace(replace_dict,
                                                                   regex=True) + ' $  &'
    each_df['explanation'] = '$ ' + \
        each_df['explanation'].str.strip().replace(
        replace_dict, regex=True) + ' $ &'
    # each_df['status'] = each_df['status'].astype(str) + ' &'
   #  each_df['explanation score'] = each_df['explanation score'].apply(lambda x : '{0:,}'.format(x))
    mask = pd.to_numeric(each_df['explanation score']).notnull()
    each_df['explanation score'].loc[mask] = each_df['explanation score'].loc[mask].astype(np.int64)
    each_df['explanation score'] = '$ ' + \
        each_df['explanation score'].round(2).astype(str) + ' $  &'
    each_df['extraction time'] = '$ ' + \
        each_df['extraction time'].round(2).astype(str) + ' $  &'
    each_df['ltl_depth'] = '$ ' + \
        each_df['ltl_depth'].round(2).astype(str) + ' $  &'
    
    mask = pd.to_numeric(each_df['lstar explanation score']).notnull()
    each_df['lstar explanation score'].loc[mask] = each_df['lstar explanation score'].loc[mask].astype(np.int64)
    each_df['lstar states'] = '$ ' + \
        each_df['lstar states'].round(2).astype(str) + ' $ &'

    each_df['lstar explanation score'] = '$ ' + \
        each_df['lstar explanation score'].round(2).astype(str) + ' $  &'
    each_df['lstar extraction time'] = '$ ' + \
        each_df['lstar extraction time'].round(2).astype(str) + ' $  \\\\'

    
    
    print("""  
   \\begin{table}
      \\begin{center}
         \\begin{tabular}{llrrr@{\\hskip 0.4in}rrr}
            \\toprule
            Query& \\multicolumn{4}{c}{LTL} & \\multicolumn{3}{c}{DFA} \\\\
			& Explanation & Depth & Acc(\%) &  Time(s) & |Q| & Acc(\%) &  Time(s)\\\\
            \\midrule
   """)

    print(each_df[['query', 'explanation', 'ltl_depth',  'explanation score',
                   'extraction time', 'lstar states', 'lstar explanation score',
                   'lstar extraction time']].to_string(index=False, header=None))
    print("\n\n\n")

    print(""" 
            \\bottomrule
         \\end{tabular}
      \\end{center} """)
    cnt = cnt + 1
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
    print("      \\caption{Explanation of $ " + str(formula) + " $.}")
    print("      \\label{tab:example"+str(cnt)+"}")
    print("\\end{table} ")



