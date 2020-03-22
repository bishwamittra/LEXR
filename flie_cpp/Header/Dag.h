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

class Dag
{
public:


	//Attributes:------------------------------------------------------------


	/* 
	Saves the formulas which are used to generate a correct DAG.
	Remains emtpy when an incremental solver is used.
	The outer vector saves the individual subformulas:
		[0] x_lambda_n exists
		[1] x_lambda_n can only be true for one lambda
		[2] x_left_n exists only for unary and binary operators
		[3] x_left_n can only be true for one lambda
		[4] x_right_n exists only for binary operators
		[5] x_right_n can only be true for one lambda
		[6] x_lamda_1 has to be a variable
	*/
	std::vector<z3::expr_vector> formulas_Dag;
	/*
	Saves the formulas which make sure that every node has a parent.
	The outer vector saves the formulas for each node
	*/
	std::vector<z3::expr_vector> formulas_Parent_Exists;
	/*
	variables_x_lambda_i[lambda][i] should be true if and only if node i is labled with lambda
	lambda can be:
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
	std::vector<z3::expr_vector> variables_x_lambda_i;
	/*
	variables_left_i_j[i][j] should be true if and only if the left child of i is j
	*/
	std::vector<z3::expr_vector> variables_left_i_j;
	/*
	variables_left_i_j[i][j] should be true if and only if the right child of i is j
	*/
	std::vector<z3::expr_vector> variables_right_i_j;


	//Methods:---------------------------------------------------------------


	/*
	Constructor used when a new solver is created in every iteration.
		context: the context where all expressions are added
		number_Of_Variables: the number of variables each letter of each word consists of
	*/
	Dag(z3::context& context);
	/*
	Adds the new x_lambda_n, x_left and x_right to the variable pool
		iteration: is the index of the new node which is added to the DAG
	*/
	virtual void add_Variables(int iteration);
	/*
	Adds the formulas which are needed to construct a DAG with one more node.
	Adds the formulas which make sure that every node has a parent.
		iteration: is the index of the new node which is added to the DAG
	*/
	virtual void add_Formulas(int iteration);
	/*
	Is called when an incremental solver is used.
	*/
	virtual void set_Incremental(z3::solver* solver);
	/*
	Initializes all variables and formulas
	*/
	void initialize();

	void set_Number_Of_Variables(int number_Of_Variables_Input) { number_Of_Variables = number_Of_Variables_Input; };

	~Dag();

protected:


	//Attributes:------------------------------------------------------------


	/*
	The context where all expressions are added. 
	*/
	z3::context& context;
	/*
	The number of variables each letter of each word consists of
	*/
	int number_Of_Variables;
	/*
	Pointer to the solver used in the incremental case. 
	Only is defined if an incremental approach is used
	*/
	z3::solver* solver;
	/*
	Is true if an incremental approach is used.
	*/
	bool using_Incremental = false;
	/*
	#variables + 0: not
	#variables + 4: next
	#variables + 5: finally
	#variables + 6: globally
	*/
	const int unary[4] = { 0,4,5,6 };
	/*
	#variables + 1: or
	#variables + 2: and
	#variables + 3: implies
	#variables + 7: until
	*/
	const int binary[4] = { 1,2,3,7 };


	//Methods:---------------------------------------------------------------


	/*
	constructs the formulas for the first iteration
	*/
	void initialize_Dag();
};

