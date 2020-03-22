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

#include "Header/Dag.h"




Dag::Dag(z3::context & context) :
	context(context)
{
}

void Dag::initialize_Dag()
{
	z3::expr_vector disjunction_X_Exists(context);
	for (int i = 0; i < number_Of_Variables + 8; i++) {
		disjunction_X_Exists.push_back(variables_x_lambda_i[i][0]);
	}
	z3::expr dag_X_Exists = z3::atleast(disjunction_X_Exists, 1);
	//z3::expr dag_X_Exists = z3::mk_or(disjunction_X_Exists);

	z3::expr_vector vector_X_Exclusive(context);
	for (int i = 0; i < number_Of_Variables + 8; i++) {
		vector_X_Exclusive.push_back(variables_x_lambda_i[i][0]);
	}
	z3::expr dag_X_Exclusive = z3::atmost(vector_X_Exclusive, 1);
		/*z3::expr_vector vector_X_Exclusive(context);
	for (int i = 0; i < number_Of_Variables + 8; i++) {
		for(int j = i+1; j < number_Of_Variables +8; j++)
		vector_X_Exclusive.push_back(!variables_x_lambda_i[i][0] || !variables_x_lambda_i[j][0]);
	}
	z3::expr dag_X_Exclusive = z3::mk_and(vector_X_Exclusive);*/
	

	z3::expr_vector disjunction_X1_Variable(context);
	for (int i = 0; i < number_Of_Variables; i++) {
		disjunction_X1_Variable.push_back(variables_x_lambda_i[i][0]);
	}
	//z3::expr dag_X1_Variable = z3::atleast(disjunction_X1_Variable, 1);
	z3::expr dag_X1_Variable = z3::mk_or(disjunction_X1_Variable);

	if (using_Incremental) {

		solver->add(dag_X_Exists);
		solver->add(dag_X_Exclusive);
		solver->add(dag_X1_Variable);
	}
	else {
		formulas_Dag[0].push_back(dag_X_Exists);
		formulas_Dag[1].push_back(dag_X_Exclusive);
		formulas_Dag[6].push_back(dag_X1_Variable);
	}
}

void Dag::add_Variables(int iteration)
{

	// add the x_lambda_n
	for (int i = 0; i < 8 + number_Of_Variables; i++) {
		std::stringstream int_To_String;
		int_To_String << "x_" << i << "_" << iteration; // making the variable name first index stands for operator second for 1..n	
		variables_x_lambda_i[i].push_back(context.bool_const(int_To_String.str().c_str())); // adding variable to the context and saving it in the vector
	}

	// add the left_n_j
	z3::expr_vector variables_Left(context);
	for (int i = 0; i < iteration; i++) {
		std::stringstream int_To_String;
		int_To_String << "l_" << iteration << "_" << i;
		variables_Left.push_back(context.bool_const(int_To_String.str().c_str()));
	}
	variables_left_i_j.push_back(variables_Left);

	//add the right_n_j
	z3::expr_vector variables_Right(context);;
	for (int i = 0; i < iteration; i++) {
		std::stringstream int_To_String;
		int_To_String << "r_" << iteration << "_" << i;
		variables_Right.push_back(context.bool_const(int_To_String.str().c_str()));
	}
	variables_right_i_j.push_back(variables_Right);
}

void Dag::add_Formulas(int iteration) {

	//node n has exactly one operator
	z3::expr_vector disjunction_X_Exists(context);
	for (int i = 0; i < number_Of_Variables + 8; i++) {
		disjunction_X_Exists.push_back(variables_x_lambda_i[i][iteration]);
	}
	z3::expr dag_X_Exists = z3::atleast(disjunction_X_Exists, 1);
	//z3::expr dag_X_Exists = z3::mk_or(disjunction_X_Exists);

	
	z3::expr_vector vector_X_Exclusive(context);
	for (int i = 0; i < number_Of_Variables + 8; i++) {
		vector_X_Exclusive.push_back(variables_x_lambda_i[i][iteration]);

	}
	z3::expr dag_X_Exclusive = z3::atmost(vector_X_Exclusive, 1);
		/*z3::expr_vector vector_X_Exclusive(context);
	for (int i = 0; i < number_Of_Variables + 8; i++) {
		for (int j = i+1; j < number_Of_Variables + 8; j++)
			vector_X_Exclusive.push_back(!variables_x_lambda_i[i][iteration] || !variables_x_lambda_i[j][iteration]);
	}
	z3::expr dag_X_Exclusive = z3::mk_and(vector_X_Exclusive);*/
	


	//subformulas constaining the operator of node n to be unary,binary or a variable
	//z3::expr node_n_Variable = context.bool_val(false);
	z3::expr_vector vector_Variable(context);
	for (int op = 0; op < number_Of_Variables; op ++) {
		vector_Variable.push_back(variables_x_lambda_i[op][iteration]);
	}
	z3::expr node_n_Variable = z3::mk_or(vector_Variable);

	z3::expr_vector vector_Unary(context);
	for (int op : unary) {
		vector_Unary.push_back(variables_x_lambda_i[number_Of_Variables + op][iteration]);
	}
	z3::expr node_n_unary = z3::mk_or(vector_Unary);

	z3::expr_vector vector_Binary(context);
	for (int op : binary) {
		vector_Binary.push_back(variables_x_lambda_i[number_Of_Variables + op][iteration]);
	}
	z3::expr node_n_binary = z3::mk_or(vector_Binary);


	// node n has exactly one left child if it is at least unary
	z3::expr_vector left_Exists(context);
	for (int j = 0; j < iteration; j++) {
		left_Exists.push_back(variables_left_i_j[iteration][j]);
	}
	z3::expr dag_Left_Exists = z3::implies(node_n_unary || node_n_binary, z3::atleast(left_Exists, 1));
	//dag_Left_Exists = (dag_Left_Exists);
	
	
	z3::expr_vector left_Exclusive(context);
	for (int j = 0; j < iteration; j++) {
		left_Exclusive.push_back(variables_left_i_j[iteration][j]);
	}
		/*z3::expr_vector left_Exclusive(context);
	for (int j = 0; j < iteration; j++) {
		for (int k = j + 1; k < iteration; k++) {
			left_Exclusive.push_back(!variables_left_i_j[iteration][j] || !variables_left_i_j[iteration][k]);
		}
	}*/
	z3::expr dag_Left_Exclusive = z3::implies(node_n_unary || node_n_binary, z3::atmost(left_Exclusive,1));
		


	// node n has exactly one right child if it is binary
	z3::expr_vector right_Exists(context);
	for (int j = 0; j < iteration; j++) {
		right_Exists.push_back(variables_right_i_j[iteration][j]);
	}
	z3::expr dag_Right_Exists = z3::implies(node_n_binary, z3::atleast(right_Exists, 1));
	//dag_Right_Exists = (dag_Right_Exists && (z3::implies(node_n_Variable || node_n_unary, !z3::mk_or(right_Exists))));

	

	z3::expr variable_No_Parents = z3::implies(node_n_Variable, !z3::mk_or(left_Exists) && !z3::mk_or(right_Exists));
	z3::expr unary_No_Right = z3::implies(node_n_unary, !z3::mk_or(right_Exists));
	
	
	z3::expr_vector right_Exclusive(context);
	for (int j = 0; j < iteration; j++) {
		right_Exclusive.push_back(variables_right_i_j[iteration][j]);
	}
		/*z3::expr_vector right_Exclusive(context);
	for (int j = 0; j < iteration; j++) {
		for (int k = j + 1; k < iteration; k++) {
			right_Exclusive.push_back(!variables_right_i_j[iteration][j] || !variables_right_i_j[iteration][k]);
		}
	}*/
	z3::expr dag_Right_Exclusive = z3::implies(node_n_binary, z3::atmost(right_Exclusive,1));
	



	// all nodes 1...n-1 may have n as a parent
	formulas_Parent_Exists.push_back(z3::expr_vector(context)); // representing node n-1
	for (unsigned int j = 0; j < formulas_Parent_Exists.size(); j++) {
		formulas_Parent_Exists[j].push_back(variables_left_i_j[iteration][j]);
		formulas_Parent_Exists[j].push_back(variables_right_i_j[iteration][j]);
	}




	if (using_Incremental) {
		solver->add(dag_X_Exists);
		solver->add(dag_X_Exclusive);
		solver->add(dag_Left_Exists);
		solver->add(dag_Left_Exclusive);
		solver->add(dag_Right_Exists);
		solver->add(dag_Right_Exclusive);
	}
	else {
		formulas_Dag[0].push_back(dag_X_Exists);
		formulas_Dag[1].push_back(dag_X_Exclusive);
		formulas_Dag[2].push_back(dag_Left_Exists);
		formulas_Dag[3].push_back(dag_Left_Exclusive);
		formulas_Dag[4].push_back(dag_Right_Exists);
		formulas_Dag[5].push_back(dag_Right_Exclusive);
		formulas_Dag[2].push_back(variable_No_Parents);
		formulas_Dag[2].push_back(unary_No_Right);

	}
}	

void Dag::set_Incremental(z3::solver * solver)
{
	using_Incremental = true;
	this->solver = solver;
}

void Dag::initialize()
{
	// set up vector to store variables;
	for (int i = 0; i < number_Of_Variables + 8; i++) {
		variables_x_lambda_i.push_back(z3::expr_vector(context));
	}

	// set up the data structure to store the formulas
	if (!using_Incremental) {
		formulas_Dag.push_back(z3::expr_vector(context));
		formulas_Dag.push_back(z3::expr_vector(context));
		formulas_Dag.push_back(z3::expr_vector(context));
		formulas_Dag.push_back(z3::expr_vector(context));
		formulas_Dag.push_back(z3::expr_vector(context));
		formulas_Dag.push_back(z3::expr_vector(context));
		formulas_Dag.push_back(z3::expr_vector(context));
	}
	
	add_Variables(0);
	initialize_Dag();
}

Dag::~Dag()
{
	formulas_Dag.clear();
}
