import os

benchmarks = [
    "Example1",
    "Example2",
    "Example3",
    "Example4",
    "Example5",
    "Example6",
    # "Example7",
    "Alternating_Bit_Protocol",
    "Email",
    "Balanced_Parentheses",
    "Text_Classification"
]

for benchmark in benchmarks:
    cmd = "python3 query_construct.py --benchmarks=" + benchmark
    print(cmd)
    os.system(cmd)