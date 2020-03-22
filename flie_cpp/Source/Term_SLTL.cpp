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

#include "Header/Term_SLTL.h"

int Term_SLTL::max_Constant = -1;



Term_SLTL::Term_SLTL(std::string & input_Line)
{
	std::stringstream string_stream(input_Line);
	std::string op;
	std::string left;
	std::string right;

	std::getline(string_stream, op, '(');
	oper = op.at(0);
	if (oper == 's') {
		op.erase(op.begin());
		var = std::stoi(op);
	}
	else if (oper == 'c') {
		op.erase(op.begin());
		var = std::stoi(op);
		if (var > max_Constant) max_Constant = var;
	}
	else {

		std::string remaining;
		std::getline(string_stream, remaining);

		int brackets = 0;
		for (unsigned int i = 0; i < remaining.size(); i++) {

			char c = remaining.at(i);

			switch (c) {
			case '(':
				brackets++;
				break;
			case ')':
				brackets--;
				break;
			case ',':
				if (brackets == 0) {
					left = remaining.substr(0, i);
					remaining.erase(remaining.begin(), remaining.begin() + i + 1);
					goto make_Right;
				}
			default:
				break;
			}
		}

	make_Right:

		remaining.erase(remaining.end() - 1);
		right = remaining;


		left_Term = new Term_SLTL(left);
		right_Term = new Term_SLTL(right);

	}
}


z3::expr Term_SLTL::compute_Term(std::vector<std::string>& signals, z3::expr_vector& constants, z3::context& context) {


	z3::expr left(context);
	z3::expr right(context);
	z3::expr result(context);

	if (oper != 'c' && oper != 's') {

		left = left_Term->compute_Term(signals, constants, context);
		right = right_Term->compute_Term(signals, constants, context);
	}

	switch (oper) {
	case '<':
		result = (left < right);
		return result;
	case '>':
		return (left_Term->compute_Term(signals, constants, context) > right_Term->compute_Term(signals, constants, context));
	case '=':
		return (left_Term->compute_Term(signals, constants, context) == right_Term->compute_Term(signals, constants, context));
	case '!':
		return (left_Term->compute_Term(signals, constants, context) != right_Term->compute_Term(signals, constants, context));
	case '+':
		return (left_Term->compute_Term(signals, constants, context) + right_Term->compute_Term(signals, constants, context));
	case '*':
		return (left_Term->compute_Term(signals, constants, context) * right_Term->compute_Term(signals, constants, context));
	case '-':
		return (left_Term->compute_Term(signals, constants, context) - right_Term->compute_Term(signals, constants, context));
	case 'c':
		return constants[var];
	default:
		return context.real_val(signals[var].c_str());
	}
}


std::string Term_SLTL::print_Term(z3::model& model, z3::expr_vector& constants) {
	std::stringstream result;

	if (oper != 'c' && oper != 's') {
		result << "(";
		result << left_Term->print_Term(model, constants);
		result << oper;
		result << right_Term->print_Term(model, constants);
		result << ")";
	}
	else {


		result << oper;
		result << var;
		if (oper == 'c') {
			result << "(";
			result << model.eval(constants[var]);

			result << ")";
		}
	}

	formula = result.str();
	return formula;
}
