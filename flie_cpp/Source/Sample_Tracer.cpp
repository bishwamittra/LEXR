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

#include "Header/Sample_Tracer.h"

Sample_Tracer::Sample_Tracer(z3::context & context, Dag& dag, std::string sample_Name) :
							all_Formulas(context), sample_Name(sample_Name), context(context), dag(dag)
{
}

void Sample_Tracer::add_Variables(int iteration)
{
	//add the Y_word_n_t
	int word_Index = 0;
	for (std::pair<int, int> word : sample_Sizes) {
		z3::expr_vector temp(context);
		for (int t = 0; t < word.first; t++) {
			std::stringstream int_To_String;
			int_To_String << "Y_" << sample_Name << "_" << word_Index << "_" << iteration << "_" << t;
			temp.push_back(context.bool_const(int_To_String.str().c_str()));
		}
		variables_Y_Word_i_t[word_Index].push_back(temp);
		word_Index++;
	}

}

void Sample_Tracer::add_Formulas(int iteration)
{
	add_Formulas_Atomic(iteration);

	add_Formulas_Not(iteration);

	add_Formulas_Or(iteration);

	add_Formulas_And(iteration);

	add_Formulas_Implies(iteration);

	add_Formulas_Next(iteration);

	add_Formulas_Finally(iteration);

	add_Formulas_Globally(iteration);

	add_Formulas_Until(iteration);
}

void Sample_Tracer::set_Incremental(z3::solver* solver)
{
	this->solver = solver;
	using_Incremental = true;
}

void Sample_Tracer::add_Formulas_Not(int iteration) {

	Operator_Not operator_Not = Operator_Not();
	make_Formula_Unary(operator_Not, iteration, 0);
	
}

void Sample_Tracer::add_Formulas_Atomic(int iteration)
{
}

void Sample_Tracer::add_Formulas_Or(int iteration)
{

	Operator_Or operator_Or = Operator_Or();
	make_Formula_Binary(operator_Or, iteration, 1);
	
}

void Sample_Tracer::add_Formulas_And(int iteration)
{

	Operator_And operator_And = Operator_And();
	make_Formula_Binary(operator_And, iteration, 2);
	
}

void Sample_Tracer::add_Formulas_Implies(int iteration)
{

	Operator_Implies operator_Implies = Operator_Implies();
	make_Formula_Binary(operator_Implies, iteration, 3);
	
}

void Sample_Tracer::add_Formulas_Next(int iteration)
{
	Operator_Next operator_Next = Operator_Next();
	make_Formula_Unary(operator_Next, iteration, 4);
	
}

void Sample_Tracer::add_Formulas_Finally(int iteration)
{
	Operator_Finally operator_Finally = Operator_Finally();
	make_Formula_Unary(operator_Finally, iteration, 5);
}

void Sample_Tracer::add_Formulas_Globally(int iteration)
{

	Operator_Globally operator_Globally = Operator_Globally();
	make_Formula_Unary(operator_Globally, iteration, 6);
	
}

void Sample_Tracer::add_Formulas_Until(int iteration)
{
	Operator_Until operator_Until = Operator_Until();
	make_Formula_Binary(operator_Until, iteration, 7);
}

void Sample_Tracer::make_Formula_Unary(Operator_Unary& op, int iteration, int operator_Index)
{

	int word_Index = 0;
	for (std::pair<int, int> word : sample_Sizes) {

		z3::expr operator_Expr(context);

		z3::expr_vector left_Conjunction(context);
		for (int j = 0; j < iteration; j++) {
			z3::expr inner_Formula = op.make_Inner_Formula(iteration, j, word_Index, context, word.first, word.second, variables_Y_Word_i_t);
			z3::expr implication = z3::implies(dag.variables_left_i_j[iteration][j], inner_Formula);
			left_Conjunction.push_back(implication);
		}
		//operator_Expr = z3::implies(variables_x_lambda_i[number_Of_Variables + operator_Index][iteration], z3::atleast(left_Conjunction, left_Conjunction.size()));
		operator_Expr = z3::implies(dag.variables_x_lambda_i[number_Of_Variables + operator_Index][iteration], z3::mk_and(left_Conjunction));
		if (using_Incremental) {
			solver->add(operator_Expr);
		}
		else {
			all_Formulas.push_back(operator_Expr);
		}
		word_Index++;
	}
}

void Sample_Tracer::make_Formula_Binary(Operator_Binary& op, int iteration, int operator_Index)
{
	int word_Index = 0;
	for (std::pair<int, int> word : sample_Sizes) {

		z3::expr operator_Expr(context);

		z3::expr_vector outer_Conjunction(context);
		for (int j = 0; j < iteration; j++) {
			for (int k = 0; k < iteration; k++) {
				z3::expr inner_Formula = op.make_Inner_Formula(iteration, j, k, word_Index, context, word.first, word.second, variables_Y_Word_i_t);
				z3::expr implication = z3::implies(dag.variables_left_i_j[iteration][j] && dag.variables_right_i_j[iteration][k], inner_Formula);
				outer_Conjunction.push_back(implication);
			}
		}
		//operator_Expr = z3::implies(variables_x_lambda_i[number_Of_Variables + operator_Index][iteration], z3::atleast(outer_Conjunction, outer_Conjunction.size()));
		
		operator_Expr = z3::implies(dag.variables_x_lambda_i[number_Of_Variables + operator_Index][iteration], z3::mk_and(outer_Conjunction));

		if (using_Incremental) {
			solver->add(operator_Expr);
		}
		else {
			all_Formulas.push_back(operator_Expr);
		}
		word_Index++;
	}
}

void Sample_Tracer::initialize()
{
}

Sample_Tracer::~Sample_Tracer()
{


	variables_Y_Word_i_t.clear();
}
