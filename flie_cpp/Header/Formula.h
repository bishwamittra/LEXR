/*
MIT License

Copyright (c) [2019] [Joshua Blickensdörfer]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

#pragma once
#include <vector>
#include <z3++.h>
#include <time.h>
#include "Header/Grammar.h"
#include "Header/Dag.h"
#include "Header/Sample_Tracer.h"
#include <memory>


/*
Structure to represent the DAG.
*/
struct Node
{
	int formula;
	Node *left;
	Node *right;
};

/*
Class which can handle solver and optimizer
*/
class Solve_And_Optimize {
public:	

	bool using_Optimize = false;
	
	Solve_And_Optimize(){}

	virtual void add(z3::expr expr) {}

	virtual void add(z3::expr expr, int weight) {}

};

class Sat_Solver:public Solve_And_Optimize{

public:
	z3::solver& solver;


	Sat_Solver(z3::solver& solver):solver(solver){};

	void add(z3::expr expr){
		solver.add(expr);
	}
};

class Max_Sat_Solver:public Solve_And_Optimize{

public:
	z3::optimize& optimize;

	Max_Sat_Solver(z3::optimize& optimize):optimize(optimize) {using_Optimize = true;}

	void add(z3::expr expr){
		optimize.add(expr);
	}

	void add(z3::expr expr, int weight) {
		optimize.add(expr, weight);
	}
};



class Formula
{
public:


	//Methods:---------------------------------------------------------------

	
	Formula();
	/*
	Find a LTL formula fullfilling all requirements.
	*/
	std::string find_LTL();

	/*
	Set the grammar if a grammar is used.
	*/
	void set_Grammar(std::vector<std::string>& grammar);

	/*
	Adds all formulas for the first iteration of the algorithm.
	*/
	void initialize();

	/*
	Sets the iteration in which an optimizer is used instead of a solver.
		optimized_Run: the iteration in which an optimizer should be used
	*/
	void set_Optimized_Run(int optimized_Run) {this->optimized_Run = optimized_Run;};

	/*
	Sets the setting of all data structures to use an incremental solver and constructs this solver.
	*/
	void set_Using_Incremental();

	void set_Vebose(int verbose) { this->verbose = verbose;};

	~Formula();	


protected:


	//Attributes:------------------------------------------------------------

	/*
	The higher verbose is the more outputs are made.
	*/
	int verbose = 0;

	/*
	The current iteration.
	*/
	int iteration = 0;

	/*
	Is true when a grammar is used.
	*/
	bool using_Grammar = false;

	/*
	The iteration in which an optimizer instead of a solver is used. (1,...)
	*/
	int optimized_Run = 0;

	/*
	The number of variables used in each letter.
	*/
	int number_Of_Variables;

	/*
	Is true if an incremental solver is used
	*/
	bool using_Incremental = false;

	/*
	The context where all expressions are added.
	*/
	z3::context context;

	/*
	Pointer to the solver used in the incremental case.
	Only is defined if an incremental approach is used
	*/
	z3::solver* solver;

	/*
	Contains all formulas and variables for the positive sample.
	*/
	std::unique_ptr<Sample_Tracer> positive_Sample;

	/*
	Contains all formulas and variables for the negative sample.
	*/
	std::unique_ptr<Sample_Tracer> negative_Sample;

	/*
	Contains all formulas and variables for the DAG.
	*/
	std::unique_ptr<Dag> dag;

	/*
	Contains all formulas and variables for the grammar.
	*/
	std::unique_ptr<Grammar> context_Free_Grammar;

	/*
	Used in order to take the time
	*/
	clock_t start;

	/*
	Used in order to take the time
	*/
	clock_t finish;

	/*
	Used in order to take the time
	*/
	double z3_Time;

	/*
	Used in order to take the time
	*/
	double own_Execution_Time;

	/*
	Is true if and only if a SLTL file should be examined
	*/
	bool using_SLTL = false;

	/*
	Is true if and only if a LTL file should be examined
	*/
	bool using_LTL = false;
	

	//Methods:---------------------------------------------------------------


	/*
	Add all the new variables for the next iteration.
	*/
	void add_Variables();

	/*
	Prepares all variables and formulas for the next iteration.
	*/
	void prepare_New_Iteration();

	/*
	Builds the tree from the satisfying assignment.
		model: the satisfying assignment
		root: index of the current node
		node_Vector: array containing pointers to all the constructed nodes
		touched: vector	saying wether a node was already constructed
	*/
	virtual Node* build_Tree(z3::model &model, int root, Node** node_Vector, std::vector<bool>& touched);

	/*
	Solves the current iteration.
	*/
	std::pair<bool, std::string> solve_Iteration();

	/*
	Solves the current iteration with an incremental solver.
	*/
	std::pair<bool, std::string> solve_Iteration_Incrementally();

	/*
	Solves the current iteration with an optimizer.
	*/
	std::pair<bool, std::string> solve_Iteration_Optimize();

	/*
	Constructs a string representing the formula of the tree.
		root: root of the tree
	*/
	virtual std::string print_Tree(Node *root);

	/*
	Adds all formulas to the Solver/Optimizer and checks the satisfiablility
	*/
	void add_Formulas(Solve_And_Optimize& solver_Optimizer);

	/*
	Creates the tree and Formula when everything is satisfiable
	*/
	void make_Result(z3::model& model, std::pair<bool, std::string>& result);

	/*
	sets the using_LTL variable to be true
	*/
	void set_LTL() { using_LTL = true; };

	/*
	sets the using_SLTL variable to be true
	*/
	void set_STL() { using_SLTL = true; };
};



