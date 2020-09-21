import pdb
from z3 import *
import argparse
from samples2ltl.smtEncoding.dagSATEncoding import DagSATEncoding
import os
from samples2ltl.solverRuns import run_solver, run_dt_solver
from samples2ltl.utils.Traces import Trace, ExperimentTraces
from multiprocessing import Process, Queue
import logging
from samples2ltl.utils.SimpleTree import SimpleTree, Formula


def helper(m, d, vars):
    tt = { k : m[vars[k]] for k in vars if k[0] == d }
    return tt



 
def learnLTL(tracesFileName="dummy.trace", startDepth=1, optimization = False):
    
    parser = argparse.ArgumentParser()
    # parser.add_argument("--traces", dest="tracesFileName", default="samples2ltl/traces/dummy.trace")
    parser.add_argument("--max_depth", dest="maxDepth", default='50')
    parser.add_argument("--start_depth", dest="startDepth", default='1')
    parser.add_argument("--max_num_formulas", dest="numFormulas", default='1')
    parser.add_argument("--iteration_step", dest="iterationStep", default='1')
    parser.add_argument("--test_dt_method", dest="testDtMethod", default=False, action='store_true')
    parser.add_argument("--test_sat_method", dest="testSatMethod", default=False, action='store_true')
    parser.add_argument("--timeout", dest="timeout", default=10, help="timeout in seconds")
    # parser.add_argument("--log", dest="loglevel", default="INFO")
    parser.add_argument("--log", dest="loglevel", default="INFO")
    
    args,unknown = parser.parse_known_args()
    # tracesFileName = args.tracesFileName
    
    
    """
    traces is 
     - list of different recorded values (traces)
     - each trace is a list of recordings at time units (time points)
     - each time point is a list of variable values (x1,..., xk) 
    """
    
    # numeric_level = args.loglevel.upper()
    # logging.basicConfig(level=numeric_level)

    
    maxDepth = int(args.maxDepth)
    numFormulas = int(args.numFormulas)
    # startDepth = int(args.startDepth)
    traces = ExperimentTraces()
    iterationStep = int(args.iterationStep)
    traces.readTracesFromFile(tracesFileName)
    finalDepth = int(args.maxDepth)

    # default formulas
    if(len(traces.acceptedTraces)==0):
        return [Formula(formulaArg='false')],1
    if(len(traces.rejectedTraces)==0):
        return [Formula(formulaArg='true')],1
    
    
    solvingTimeout = int(args.timeout)
    timeout = int(args.timeout)

    
    # print("\n\nLearning LTL: (start) ")
    # if args.testSatMethod == True:
    [formulas , formula_depth, timePassed] = run_solver(finalDepth=maxDepth, traces=traces, maxNumOfFormulas = numFormulas, startValue=startDepth, step=iterationStep, optimization=optimization)
    logging.info("formulas: "+str([f.prettyPrint(f) for f in formulas])+", timePassed: "+str(timePassed))


    # print("Learning LTL: (complete)\n")
        
    
    if args.testDtMethod == True:
        
        [timePassed, numAtoms, numPrimitives] = run_dt_solver(traces=traces)
        logging.info("timePassed: {0}, numAtoms: {1}, numPrimitives: {2}".format(str(timePassed), str(numAtoms), str(numPrimitives)))
        
    
    
    return formulas, formula_depth

if __name__ == "__main__":
    print(learnLTL())

