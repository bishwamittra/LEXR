# LEXR

LEXR is a formal description language based framework for explaining recurrent neural networks (RNNs) using Linear Temporal Logic (LTL). 

## Install
The source code is tested in Python 3.7.4 and has following dependencies.
 - [Dynet](https://dynet.readthedocs.io/en/latest/python.html)
 - [Mona](http://www.brics.dk/mona/)
 - [Z3 solver](https://github.com/Z3Prover/z3) python binding
 - run `pip install -r requirements.txt` to install all necessary python packages available from pip

 ## Directories
 - `RNN2DFA`: contains the implementation of the DFA learner and the training of RNN.
 - `samples2ltl`: contains the implementation of the LTL learner.
 - `PACTeacher`: contains the  implementation of the PAC teacher.
 - `model`: contains already trained models used in the paper.
 - `benchmarks`: contains the  benchmarks used in the paper.
 - `cluster_results`: contains the experimental results (reported in the paper) in a CSV file. Copy `cluster_results/result.csv` to `output/` for analyzing the results. The detail is below.
 - `output`: contains the experimental results in a CSV file. 


 ## Description of scripts
 - `test.py`: This script is the starting point for reproducing results. Run `python test.py --random --demo --thread=6` to generate results for the language `G(a)`. To get a detailed results for the six reported benchmarks in the paper, run `python test.py --random --thread=[0-5]`. Output is generated in the `output/` directory.  
 - Use the python notebook `_test.ipynb` for documentation.
 - `read_output.ipynb`: use this script to analyze the results. 



