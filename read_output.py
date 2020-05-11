import pandas as pd
import numpy as np
df = pd.read_csv("output/result.csv", header=None)
df.columns = ['target',
              'query',
              'explanation',
              'status',
              'rnn score',
              'explanation score',
              'explanation score on ground truth',
              'extraction time',
              'revised delta',
              'revised epsilon',
              'counterexamples',
              'train size',
              'test size'
              ]

# read email_match
email_df = df[df['target'] == "email match"][[
    'query', 'explanation', 'status','explanation score', 'extraction time']]
replace_dict = dict(zip([
    "X",
    "U",
    "F",
    "G",
    "d",
    "&",
    "~",
    "->",
    "true",
    "false",
    "a"
], [
    "\\\\X",
    "\\\\U",
    "\\\\F",
    "\\\\G",
    "\\\\circ",
    " \\\\wedge ",
    " \\\\neg ",
    " \\\\rightarrow",
    "\\\\top",
    "\\\\bot",
    "@"
]))
email_df['query'] = '$ ' + email_df['query'].str.strip().replace(replace_dict,
                                                                 regex=True) + ' $  &'
email_df['explanation'] = '$ ' + \
    email_df['explanation'].str.strip().replace(
        replace_dict, regex=True) + ' $  &'
email_df['status'] = email_df['status'].astype(str) + ' &'
mask = pd.to_numeric(email_df['explanation score']).notnull()
email_df['explanation score'].loc[mask] = email_df['explanation score'].loc[mask].astype(np.int64)

email_df['explanation score'] = '$ ' + \
    email_df['explanation score'].round(2).astype(str) + ' $  &'
email_df['extraction time'] = '$ ' + \
    email_df['extraction time'].round(2).astype(str) + ' $  \\\\'
pd.options.display.max_colwidth = 200


print("""  
   \\begin{table}
      \\begin{center}
         \\begin{tabular}{llcrr}
            \\toprule
            Query & Explanation & Completeness & Accuracy(\\%) &  Time(s)\\\\
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











bp_df = df[df['target'] == "balanced parentheses"][[
    'query', 'explanation', 'status', 'explanation score', 'extraction time']]
replace_dict = dict(zip([
    #    "d",
    "X",
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
bp_df['status'] = bp_df['status'].astype(str) + ' &'
mask = pd.to_numeric(bp_df['explanation score']).notnull()
bp_df['explanation score'].loc[mask] = bp_df['explanation score'].loc[mask].astype(np.int64)

bp_df['explanation score'] = '$ ' + \
    bp_df['explanation score'].round(2).astype(str) + ' $  &'
bp_df['extraction time'] = '$ ' + \
    bp_df['extraction time'].round(2).astype(str) + ' $  \\\\'
pd.options.display.max_colwidth = 200


print("""  
   \\begin{table}
      \\begin{center}
         \\begin{tabular}{llcrr}
            \\toprule
            Query & Explanation & Completeness & Accuracy(\\%) &  Time(s)\\\\
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









abp_df = df[df['target'] == "alternating bit protocol"][[
    'query', 'explanation', 'status', 'explanation score', 'extraction time']]
replace_dict = dict(zip([
    #    "d",
    "b",
    "X",
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
abp_df['status'] = abp_df['status'].astype(str) + ' &'
mask = pd.to_numeric(abp_df['explanation score']).notnull()
abp_df['explanation score'].loc[mask] = abp_df['explanation score'].loc[mask].astype(np.int64)

abp_df['explanation score'] = '$ ' + \
    abp_df['explanation score'].round(2).astype(str) + ' $  &'
abp_df['extraction time'] = '$ ' + \
    abp_df['extraction time'].round(2).astype(str) + ' $  \\\\'
pd.options.display.max_colwidth = 200




print("""  
   \\begin{table}
      \\begin{center}
         \\begin{tabular}{llcrr}
            \\toprule
            Query & Explanation & Completeness & Accuracy(\\%) &  Time(s)\\\\
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
                       (df['target'] != "balanced parentheses")]

cnt = 0
for formula, each_df in other_examples_df.groupby(['target']):
    replace_dict = dict(zip([
        #    "d",
        "X",
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
    each_df['status'] = each_df['status'].astype(str) + ' &'
   #  each_df['explanation score'] = each_df['explanation score'].apply(lambda x : '{0:,}'.format(x))
    mask = pd.to_numeric(each_df['explanation score']).notnull()
    each_df['explanation score'].loc[mask] = each_df['explanation score'].loc[mask].astype(np.int64)

    each_df['explanation score'] = '$ ' + \
        each_df['explanation score'].round(2).astype(str) + ' $  &'
    each_df['extraction time'] = '$ ' + \
        each_df['extraction time'].round(2).astype(str) + ' $  \\\\'
    pd.options.display.max_colwidth = 200

    print("""  
   \\begin{table}
      \\begin{center}
         \\begin{tabular}{llcrr}
            \\toprule
            Query & Explanation & Completeness & Accuracy(\\%) &  Time(s)\\\\
            \\midrule
   """)

    print(each_df[['query', 'explanation', 'status', 'explanation score',
                   'extraction time']].to_string(index=False, header=None))
    print("\n\n\n")

    print(""" 
            \\bottomrule
         \\end{tabular}
      \\end{center} """)
    cnt = cnt + 1
    replace_dict = dict(zip([
        #    "d",
        "X",
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
