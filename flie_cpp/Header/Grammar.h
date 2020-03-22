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
#include <z3++.h>
#include "Header/Dag.h"

struct Form {
	std::string oper;
	int left;
	int right;
};

class Grammar
{
public:


	//Attributes:------------------------------------------------------------


	/*
	Contains all formulas making sure that the formula represented by the dag can be 
	derived by the grammar.
	*/
	z3::expr_vector formulas_Grammar;


	//Methods:---------------------------------------------------------------


	/*
	Constructer used when in each iteration a new solver is constructed
		context: the context where all expressions are added
		number_Of_Variables: the number of variables each letter of each word consists of
		grammar: the grammar
		dag: formulas and variables used to represent the DAG
	*/
	Grammar(z3::context& context, Dag& dag, int number_Of_Variables, std::vector<std::string>& grammar_String);


	/*
	Adds the formulas which are needed to make sure that the DAG is compliant with the grammar
		iteration: is the index of the new node which is added to the DAG
	*/
	void add_Formulas(int iteration);
	/*
	Adds the variables of the grammar
	iteration: is the index of the new node which is added to the DAG
	*/
	void add_Variables(int iteration);
	/*
	Constructs the formula that the root of the tree is constructed by a
	production rule from N_1
		iteration: index of the root node
	*/
	z3::expr make_Start(int iteration);

	/*
	Adds the formulas for the first iteration.
	*/
	void initialize();

	void set_Incremental(z3::solver* solver) { this->solver = solver; };

	void set_Number_Of_Variables(int number_Of_Variables) { this->number_Of_Variables = number_Of_Variables; };


	~Grammar();

protected:


	//Attributes:------------------------------------------------------------


	/*
	Pointer to the solver used in the incremental case.
	Only is defined if an incremental approach is used
	*/
	z3::solver* solver;
	/*
	The context where all expressions are added.
	*/
	z3::context& context;
	/*
	The number of variables each letter of each word consists of
	*/
	int number_Of_Variables;
	/*
	Number of Nonterminals of the grammar
	*/
	int number_Of_Nonterminals;
	/*
	Formulas and variables used to represent the DAG.
	*/
	Dag& dag;
	/*
	variables_S_i_k_q[i][k][q] should be true if and only if node i is derived by using 
	production rule N_k -> F_k_q
	*/
	std::vector<std::vector<z3::expr_vector> > variables_S_i_k_q;
	/*
	map_To_Op[k][Op] contains all q with N_k -> F_k_q and the Operator
	of F_k_q is Op
	Op can be:
	0 to (#variables - 1): variable with respective index
	#variables + 0: not
	#variables + 1: or
	#variables + 2: and
	#variables + 3: implies
	#variables + 4: next
	#variables + 5: finally
	#variables + 6: globally
	#variables + 7: until
	*/
	std::vector<std::vector<std::vector<int> > > map_To_Operators_k_Op;
	/*
	Contains the entire grammar
	*/
	std::vector<std::vector<Form> > grammar_k_q;




	//Methods:---------------------------------------------------------------

	
	/*
	Initializes the data structure variables_S_i_k_q
	*/
	void initialize_Variables_S();
	/*
	Initializes the map_To_Operators_k_Op data structure.
	Initializes grammar_k_q.
	*/
	void initialize_Grammar(std::vector<std::vector<Form> >& grammar);
	/*
	Adds the formulas making sure that exactly one S variable is satisfied.
	*/
	void add_Exactly_One(int iteration);



	std::vector<Form> make_Formulas_Grammar(std::string &input_Line);


	//TODO is this needed?
	void add_One_Dimensional_Grammar(int z, int iteration);
	void add_Two_Dimensional_Grammar(int z, int iteration);
};

