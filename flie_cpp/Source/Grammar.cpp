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

#include "Header/Grammar.h"


Grammar::Grammar(z3::context& context, Dag& dag, int number_Of_Variables, std::vector<std::string>& grammar_String) :
	formulas_Grammar(context), context(context), number_Of_Variables(number_Of_Variables), dag(dag) 
{
	
	std::vector<std::vector<Form> > grammar;
	for (std::string& line : grammar_String) {
		grammar.push_back(make_Formulas_Grammar(line));
	}

	number_Of_Nonterminals = grammar.size();


	initialize_Grammar(grammar);
	initialize_Variables_S();
	

}


void Grammar::initialize()
{
	add_Formulas(0);
}

Grammar::~Grammar()
{
}

void Grammar::initialize_Grammar(std::vector<std::vector<Form> >& grammar)
{
	for (int i = 0; i < number_Of_Nonterminals; i++) {
		std::vector<std::vector<int> > temp;
		for (int j = 0; j < number_Of_Variables + 9; j++) {
			temp.push_back(std::vector<int>());
		}
		map_To_Operators_k_Op.push_back(temp);
	}


	int nonterminal = 0;
	for (std::vector<Form> formulas : grammar) {
		int second_Index = 0;
		for (Form form : formulas) {
			if (!form.oper.compare("!")) {
				map_To_Operators_k_Op[nonterminal][number_Of_Variables].push_back(second_Index);
			}
			else if (!form.oper.compare("||")) {
				map_To_Operators_k_Op[nonterminal][number_Of_Variables + 1].push_back(second_Index);
			}
			else if (!form.oper.compare("&&")) {
				map_To_Operators_k_Op[nonterminal][number_Of_Variables + 2].push_back(second_Index);
			}
			else if (!form.oper.compare("->")) {
				map_To_Operators_k_Op[nonterminal][number_Of_Variables + 3].push_back(second_Index);
			}
			else if (!form.oper.compare("X")) {
				map_To_Operators_k_Op[nonterminal][number_Of_Variables + 4].push_back(second_Index);
			}
			else if (!form.oper.compare("F")) {
				map_To_Operators_k_Op[nonterminal][number_Of_Variables + 5].push_back(second_Index);
			}
			else if (!form.oper.compare("G")) {
				map_To_Operators_k_Op[nonterminal][number_Of_Variables + 6].push_back(second_Index);
			}
			else if (!form.oper.compare("U")) {
				map_To_Operators_k_Op[nonterminal][number_Of_Variables + 7].push_back(second_Index);
			}
			else {
				form.oper.erase(0, 1);
				map_To_Operators_k_Op[nonterminal][std::stoi(form.oper)].push_back(second_Index);
			}
			second_Index++;
		}

		grammar_k_q.push_back(formulas);
		nonterminal++;
	}
}

void Grammar::add_Exactly_One(int iteration)
{
	z3::expr_vector variables_Iteration(context);
	for (const z3::expr_vector& expr_Vec : variables_S_i_k_q[iteration]) {
		for (const z3::expr& var : expr_Vec) {
			variables_Iteration.push_back(var);
		}
	}
	formulas_Grammar.push_back(z3::atmost(variables_Iteration, 1));
	formulas_Grammar.push_back(z3::atleast(variables_Iteration, 1));

}

void Grammar::initialize_Variables_S()
{
	// grammar has to be initialized already

	std::vector<z3::expr_vector> temp1;
	for (int i = 0; i < number_Of_Nonterminals; i++) {
		z3::expr_vector temp(context);
		for (unsigned int j = 0; j < grammar_k_q[i].size(); j++) {
			std::stringstream int_To_String;
			// the first indices are for variables and the last 8 indices are for the operators
			int_To_String << "S_" << 0 << "_" << i << "_" << j; // making the variable name first index stands for operator second for 1..n
																//variables_x_lambda_i[i] = z3::expr_vector(context);
			temp.push_back(context.bool_const(int_To_String.str().c_str())); // adding variable to the context and saving it in the vector
		}
		temp1.push_back(temp);
	}
	variables_S_i_k_q.push_back(temp1);
}

void Grammar::add_Formulas(int iteration)
{

	// add Production
	for (int k = 0; k < number_Of_Nonterminals; k++) {
		for (int z = 0; z< number_Of_Variables + 7; z++) {
			for (int q : map_To_Operators_k_Op[k][z]) {

				formulas_Grammar.push_back(z3::implies(variables_S_i_k_q[iteration][k][q], dag.variables_x_lambda_i[z][iteration]));
			}
		}
	}

	add_Exactly_One(iteration);

	// add one dimensional formulas
	add_One_Dimensional_Grammar(number_Of_Variables, iteration);
	add_One_Dimensional_Grammar(number_Of_Variables + 4, iteration);
	add_One_Dimensional_Grammar(number_Of_Variables + 5, iteration);
	add_One_Dimensional_Grammar(number_Of_Variables + 6, iteration);

	// add two dimensional formulas
	add_One_Dimensional_Grammar(number_Of_Variables + 1, iteration);
	add_One_Dimensional_Grammar(number_Of_Variables + 2, iteration);
	add_One_Dimensional_Grammar(number_Of_Variables + 3, iteration);
	add_One_Dimensional_Grammar(number_Of_Variables + 7, iteration);

}

void Grammar::add_Variables(int iteration)
{
	// add the S
	std::vector<z3::expr_vector> temp1;
	for (int k = 0; k < number_Of_Nonterminals; k++) {
		z3::expr_vector temp(context);
		for (unsigned int q = 0; q < grammar_k_q[k].size(); q++) {
			std::stringstream int_To_String;
			// the first indices are for variables and the last 8 indices are for the operators
			int_To_String << "S_" << iteration << "_" << k << "_" << q; // making the variable name first index stands for operator second for 1..n
																		//variables_x_lambda_i[i] = z3::expr_vector(context);
			temp.push_back(context.bool_const(int_To_String.str().c_str())); // adding variable to the context and saving it in the vector
		}
		temp1.push_back(temp);
	}
	variables_S_i_k_q.push_back(temp1);
}

void Grammar::add_One_Dimensional_Grammar(int z, int iteration)
{
	for (int k = 0; k < number_Of_Nonterminals; k++) {
		for (int q : map_To_Operators_k_Op[k][z]) {
			z3::expr_vector conjunction(context);
			
			for (int j = 0; j < iteration; j++) {
				z3::expr_vector disjunction(context);
				int k2 = grammar_k_q[k][q].left;
				
				for (unsigned int q2 = 0; q2 < grammar_k_q[k2].size(); q2++) {
					disjunction.push_back(variables_S_i_k_q[j][k2][q2]);
					
				}
				conjunction.push_back(z3::implies((variables_S_i_k_q[iteration][k][q] && dag.variables_left_i_j[iteration][j]), z3::mk_or(disjunction)));
			}
			
			formulas_Grammar.push_back(z3::mk_and(conjunction));
			
		}
	}
}

void Grammar::add_Two_Dimensional_Grammar(int z, int iteration)
{

	for (int k = 0; k < number_Of_Nonterminals; k++) {
		for (int q : map_To_Operators_k_Op[k][z]) {
			z3::expr_vector conjunction(context);
			for (int j = 0; j < iteration; j++) {
				for (int j2 = 0; j2 < iteration; j2++) {
					z3::expr_vector disjunction(context);
					int k2 = grammar_k_q[k][q].left;
					for (unsigned int q2 = 0; q2 < grammar_k_q[k2].size(); q2++) {
						disjunction.push_back(variables_S_i_k_q[j][k2][q2]);
					}

					z3::expr_vector disjunction2(context);
					int k3 = grammar_k_q[k][q].right;
					for (unsigned int q3 = 0; q3 < grammar_k_q[k3].size(); q3++) {
						disjunction2.push_back(variables_S_i_k_q[j2][k3][q3]);
					}

					conjunction.push_back(z3::implies((variables_S_i_k_q[iteration][k][q] &&
						dag.variables_left_i_j[iteration][j] &&
						dag.variables_right_i_j[iteration][j2])
						,z3::mk_or(disjunction) && z3::mk_or(disjunction2)));
				}
			}
			formulas_Grammar.push_back(z3::mk_and(conjunction));
		}
	}
}

z3::expr Grammar::make_Start(int iteration)
{
	z3::expr disjunction = context.bool_val(false);
	for (unsigned int q = 0; q < grammar_k_q[0].size(); q++) {
		disjunction = (disjunction || variables_S_i_k_q[iteration][0][q]);
	}
	return disjunction;
}



std::vector<Form> Grammar::make_Formulas_Grammar(std::string &input_Line) {
	std::stringstream string_stream(input_Line);
	std::string word_Part;

	std::getline(string_stream, word_Part, '>');

	std::vector<Form> result;

	while (std::getline(string_stream, word_Part, ';')) {
		std::stringstream temp(word_Part);
		std::string oper;
		Form formula;
		std::getline(temp, oper, ',');
		formula.oper = oper;
		if (!oper.compare("&&") || !oper.compare("||") || !oper.compare("->") || !oper.compare("U")) {
			std::getline(temp, oper, ',');
			oper.erase(0, 1);
			formula.left = std::stoi(oper);

			std::getline(temp, oper, ',');
			oper.erase(0, 1);
			formula.right = std::stoi(oper);
		}
		else if (!oper.compare("!") || !oper.compare("F") || !oper.compare("G") || !oper.compare("X")) {
			std::getline(temp, oper, ',');
			oper.erase(0, 1);
			formula.left = std::stoi(oper);

			formula.right = -1;
		}
		else {
			formula.left = -1;
			formula.right = -1;
		}

		result.push_back(formula);
	}
	return result;
}
