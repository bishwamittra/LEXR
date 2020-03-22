/*
MIT License

Copyright (c) [2019] [Joshua Blickensd�rfer]

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
#include "Header/Dag.h"
#include <z3++.h>
#include "Header/Functor_Operators.h"

class Sample_Tracer
{
public:


	//Attributes:------------------------------------------------------------


	Sample_Tracer(z3::context& context, Dag& dag, std::string sample_Name);
	/*
	Variables_Y_Word_i_t[word_Index][i][t] should be satisfied if and only if the subformula
	starting at node i is satisfied for the word with word_Index at position t.
	*/
	std::vector<std::vector<z3::expr_vector> > variables_Y_Word_i_t;
	/*
	Saves all formulas which are used to track the satisfiability of the subformulas.
	Remains emtpy when an incremental solver is used.
	*/
	z3::expr_vector all_Formulas;


	std::vector<std::pair<int, int> > sample_Sizes;

	//Methods:---------------------------------------------------------------
	
	
	/*
	Adds the new Y_word_i_t to the variables. In this case i is iteration
		iteration: index of new root node
	*/
	virtual void add_Variables(int iteration);
	/*
	Adds the formulas making sure that the Y variables are satisfied correctly if the 
	DAG has one more node.
		iteration: index of new root node
	*/
	virtual void add_Formulas(int iteration);
	/*
	Is called when an incremental solver is used.
	*/
	virtual void set_Incremental(z3::solver* solver);
	/*
	Initializes all Variables and Formulas
	*/
	virtual void initialize();

	int get_Number_Of_Variables() {return number_Of_Variables;};

	virtual ~Sample_Tracer();

protected:


	//Attributes:------------------------------------------------------------


	/*
	Either positive or negative, depending on wether the words in the sample should be satisfied or not.
	*/
	std::string sample_Name;
	/*
	The number of variables each letter of each word consists of
	*/
	int number_Of_Variables;
	/*
	The context where all expressions are added. 
	*/
	z3::context& context;
	/*
	Pointer to the solver used in the incremental case. 
	Only is defined if an incremental approach is used
	*/
	z3::solver* solver;
	/*
	Formulas and variables used to represent the DAG.
	*/
	Dag& dag;
	/*
	Is true if an incremental approach is used.
	*/
	bool using_Incremental = false;

	

	//Methods:---------------------------------------------------------------


	void add_Formulas_Not(int iteration);

	virtual void add_Formulas_Atomic(int iteration);

	void add_Formulas_Or(int iteration);

	void add_Formulas_And(int iteration);

	void add_Formulas_Implies(int iteration);

	void add_Formulas_Next(int iteration);

	void add_Formulas_Finally(int iteration);

	void add_Formulas_Globally(int iteration);

	void add_Formulas_Until(int iteration);

	void make_Formula_Unary(Operator_Unary& op, int iteration, int operator_Index);
	void make_Formula_Binary(Operator_Binary& op, int iteration, int operator_Index);

};

