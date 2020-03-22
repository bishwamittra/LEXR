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


#include <z3++.h>
#include <vector>

class Operator_Unary {

public:
	Operator_Unary() {};
	virtual z3::expr make_Inner_Formula(int iteration, int j, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{
		return z3::expr(context);
	};
};

class Operator_Not : public Operator_Unary {

public:
	z3::expr  make_Inner_Formula(int iteration, int j, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{

		z3::expr_vector inner_Formula(context);

		for (int t = 0; t < word_Size; t++) {
			inner_Formula.push_back(variables_Y_Word_i_t[word_Index][iteration][t] ==
				(!variables_Y_Word_i_t[word_Index][j][t]));
		}

		return z3::mk_and(inner_Formula);
	}
};

class Operator_Next : public Operator_Unary {

public:
	z3::expr  make_Inner_Formula(int iteration, int j, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{

		z3::expr_vector inner_Formula(context);

		for (int t = 0; t < word_Size - 1; t++) {
			inner_Formula.push_back(variables_Y_Word_i_t[word_Index][iteration][t] ==
				variables_Y_Word_i_t[word_Index][j][t + 1]);
		}
		inner_Formula.push_back(variables_Y_Word_i_t[word_Index][iteration][word_Size - 1] ==
			variables_Y_Word_i_t[word_Index][j][repetition]);

		return z3::mk_and(inner_Formula);
	}
};

class Operator_Finally : public Operator_Unary {

public:
	z3::expr  make_Inner_Formula(int iteration, int j, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{


		z3::expr_vector conjunction_Pre_Loop(context);

		z3::expr_vector conjunction_Outer(context);
		for (int t = 0; t < word_Size; t++) {
			int s = t;
			z3::expr_vector conjunction(context);
			int stopping_Time = (t <= repetition) ? word_Size - 1 : t - 1;
			bool last_Loop_Done = false;
			while (s != stopping_Time || !last_Loop_Done) {
				if (s == stopping_Time) last_Loop_Done = true;
				conjunction.push_back(variables_Y_Word_i_t[word_Index][j][s]);
				s = (s < word_Size - 1) ? s + 1 : repetition;
			}
			conjunction_Outer.push_back(variables_Y_Word_i_t[word_Index][iteration][t] == z3::mk_or(conjunction));
		}
		z3::expr inner_Formula = z3::mk_and(conjunction_Outer);

		/*

		z3::expr_vector conjunction_Pre_Loop(context);
		for (unsigned int t = 0; t < word.second; t++) {
		z3::expr_vector disjunction(context);
		for (int s = t; s < word.first.size(); s++) {
		disjunction.push_back(variables_Y_Word_i_t[word_Index][j][s]);
		}
		conjunction_Pre_Loop.push_back(variables_Y_Word_i_t[word_Index][iteration][t] == z3::mk_or(disjunction));
		}

		z3::expr_vector conjunction_In_Loop(context);
		for (unsigned int t = word.second; t < word.first.size(); t++) {
		z3::expr_vector disjunction(context);
		for (int s = word.second; s < word.first.size(); s++) {
		disjunction.push_back(variables_Y_Word_i_t[word_Index][j][s]);
		}
		conjunction_In_Loop.push_back(variables_Y_Word_i_t[word_Index][iteration][t] == z3::mk_or(disjunction));
		}

		z3::expr inner_Formula = z3::mk_and(conjunction_In_Loop) && z3::mk_and(conjunction_Pre_Loop);
		*/
		return inner_Formula;
	}
};

class Operator_Globally : public Operator_Unary {

public:
	z3::expr  make_Inner_Formula(int iteration, int j, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{
		z3::expr_vector conjunction_Pre_Loop(context);

		z3::expr_vector conjunction_Outer(context);
		for (int t = 0; t < word_Size; t++) {
			int s = t;
			z3::expr_vector conjunction(context);
			int stopping_Time = (t <= repetition) ? word_Size - 1 : t - 1;
			bool last_Loop_Done = false;
			while (s != stopping_Time || !last_Loop_Done) {
				if (s == stopping_Time) last_Loop_Done = true;
				conjunction.push_back(variables_Y_Word_i_t[word_Index][j][s]);
				s = (s < word_Size - 1) ? s + 1 : repetition;
			}
			conjunction_Outer.push_back(variables_Y_Word_i_t[word_Index][iteration][t] == z3::mk_and(conjunction));
		}
		z3::expr inner_Formula = z3::mk_and(conjunction_Outer);




		/*
		for (unsigned int t = 0; t < word.second; t++) {
		z3::expr_vector conjunction(context);
		for (int s = t; s < word.first.size(); s++) {
		conjunction.push_back(variables_Y_Word_i_t[word_Index][j][s]);
		}
		conjunction_Pre_Loop.push_back(variables_Y_Word_i_t[word_Index][iteration][t] == z3::mk_and(conjunction));
		}

		z3::expr_vector conjunction_In_Loop(context);
		for (unsigned int t = word.second; t < word.first.size(); t++) {
		z3::expr_vector conjunction(context);
		for (int s = word.second; s < word.first.size(); s++) {
		conjunction.push_back(variables_Y_Word_i_t[word_Index][j][s]);
		}
		conjunction_In_Loop.push_back(variables_Y_Word_i_t[word_Index][iteration][t] == z3::mk_and(conjunction));
		}

		z3::expr inner_Formula = z3::mk_and(conjunction_In_Loop) && z3::mk_and(conjunction_Pre_Loop);
		*/
		return inner_Formula;
	}
};



class Operator_Binary {

public:
	Operator_Binary() {};
	virtual z3::expr make_Inner_Formula(int iteration, int j, int k, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{
		return z3::expr(context);
	};
};

class Operator_Or : public Operator_Binary {

public:
	z3::expr  make_Inner_Formula(int iteration, int j, int k, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{

		z3::expr_vector inner_Formula(context);
		for (int t = 0; t < word_Size; t++) {
			inner_Formula.push_back(variables_Y_Word_i_t[word_Index][iteration][t] ==
				(variables_Y_Word_i_t[word_Index][j][t] || variables_Y_Word_i_t[word_Index][k][t]));
		}

		return z3::mk_and(inner_Formula);
	}
};

class Operator_And : public Operator_Binary {

public:
	z3::expr  make_Inner_Formula(int iteration, int j, int k, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{

		z3::expr_vector inner_Formula(context);
		for (int t = 0; t < word_Size; t++) {
			inner_Formula.push_back(variables_Y_Word_i_t[word_Index][iteration][t] ==
				(variables_Y_Word_i_t[word_Index][j][t] && variables_Y_Word_i_t[word_Index][k][t]));
		}

		return z3::mk_and(inner_Formula);
	}
};

class Operator_Implies : public Operator_Binary {

public:
	z3::expr  make_Inner_Formula(int iteration, int j, int k, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{

		z3::expr_vector inner_Formula(context);
		for (int t = 0; t < word_Size; t++) {
			inner_Formula.push_back(variables_Y_Word_i_t[word_Index][iteration][t] ==
				z3::implies(variables_Y_Word_i_t[word_Index][j][t], variables_Y_Word_i_t[word_Index][k][t]));
		}

		return z3::mk_and(inner_Formula);
	}
};

class Operator_Until : public Operator_Binary {

public:
	z3::expr  make_Inner_Formula(int iteration, int j, int k, int word_Index,
		z3::context& context, int word_Size, int repetition,
		std::vector<std::vector<z3::expr_vector> >& variables_Y_Word_i_t)
	{

		z3::expr_vector conjunction_Loop(context);

		for (int t = 0; t < repetition; t++) {
			z3::expr_vector disjunction(context);
			for (int s = t; s < word_Size; s++) {
				z3::expr_vector conjunction(context);
				conjunction.push_back(variables_Y_Word_i_t[word_Index][k][s]);
				for (int q = t; q < s; q++) {
					conjunction.push_back(variables_Y_Word_i_t[word_Index][j][q]);
				}
				disjunction.push_back(z3::mk_and(conjunction));
			}
			conjunction_Loop.push_back(variables_Y_Word_i_t[word_Index][iteration][t] ==
				z3::mk_or(disjunction));
		}

		for (int t = repetition; t < word_Size; t++) {
			z3::expr_vector disjunction(context);
			for (int s = repetition; s < word_Size; s++) {
				z3::expr_vector conjunction(context);
				conjunction.push_back(variables_Y_Word_i_t[word_Index][k][s]);
				int q = t;
				while (q != s) {
					conjunction.push_back(variables_Y_Word_i_t[word_Index][j][q]);

					q++;
					if (q >= word_Size) {
						q = repetition;
					}
				}
				disjunction.push_back(z3::mk_and(conjunction));
			}
			conjunction_Loop.push_back(variables_Y_Word_i_t[word_Index][iteration][t] ==
				z3::mk_or(disjunction));
		}


		z3::expr inner_Formula = z3::mk_and(conjunction_Loop);

		return inner_Formula;
	}
};

