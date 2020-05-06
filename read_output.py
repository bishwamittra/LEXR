import pandas as pd
df = pd.read_csv("output/result.csv", header=None)
df.columns = ['target',
              'query',
              'explanation',
              'status',
              'rnn score',
              'explanation score',
              'explanation score on ground truth',
              'extraction time'
              ]
# only read email_match
email_df = df[df['target'] == "email match"][['query', 'explanation','status']]
replace_dict=dict(zip([
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
email_df['query'] = '$ ' + email_df['query'].str.strip().replace(replace_dict, regex=True) + ' $  &'
email_df['explanation'] = '$ ' + email_df['explanation'].str.strip().replace(replace_dict, regex=True) + ' $  &'
email_df['status'] = email_df['status'].astype(str) + ' \\\\'
pd.options.display.max_colwidth = 100
print(email_df.to_string(index=False))

print("\n\n")


bp_df = df[df['target'] == "balanced parentheses"][['query', 'explanation','status']]
replace_dict=dict(zip([ 
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
                           "\\\\X",
                           "\\\\U",
                           "\\\\F",
                           "\\\\G",
                           " \\\\wedge ", 
                           " \\\\neg ",
                           " \\\\rightarrow",
                           "\\\\top",
                           "\\\\bot",
                        #    "@"
                           ]))
bp_df['query'] = '$ ' + bp_df['query'].str.strip().replace(replace_dict, regex=True) + ' $  &'
bp_df['explanation'] = '$ ' + bp_df['explanation'].str.strip().replace(replace_dict, regex=True) + ' $ &'
bp_df['status'] = bp_df['status'].astype(str) + ' \\\\'
pd.options.display.max_colwidth = 200
print(bp_df.to_string(index=False))
print("\n\n\n")

abp_df = df[df['target'] == "alternating bit protocol"][['query', 'explanation','status']]
replace_dict=dict(zip([ 
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
                           "\\\\X",
                           "\\\\U",
                           "\\\\F",
                           "\\\\G",
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
abp_df['query'] = '$ ' + abp_df['query'].str.strip().replace(replace_dict, regex=True) + ' $  &'
abp_df['explanation'] = '$ ' + abp_df['explanation'].str.strip().replace(replace_dict, regex=True) + ' $ &'
abp_df['status'] = abp_df['status'].astype(str) + ' \\\\'
pd.options.display.max_colwidth = 200
print(abp_df.to_string(index=False))


