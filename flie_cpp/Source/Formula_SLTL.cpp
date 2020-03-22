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

#include "Header/Formula_SLTL.h"
#include "Header/Sample_Tracer_SLTL.h"



Formula_SLTL::Formula_SLTL(std::vector<std::string>& positive_Sample_String,
	std::vector<std::string>& negative_Sample_String,
	std::vector<std::string>& term_String):
	variables_Constants(context)
{
	start = clock();



	for (std::string& line : term_String) {
		terms.push_back(Term_SLTL(line));
	}

	for (int i = 0; i <= Term_SLTL::max_Constant; i++) {
		std::stringstream int_To_String;
		int_To_String << "c_" << i;
		variables_Constants.push_back(context.real_const(int_To_String.str().c_str()));
	}


	dag =  std::unique_ptr<Dag>(new Dag(context));
	positive_Sample = std::unique_ptr<Sample_Tracer>(new Sample_Tracer_SLTL(context, *dag, positive_Sample_String, "positive", variables_Constants, terms));
	negative_Sample = std::unique_ptr<Sample_Tracer>(new Sample_Tracer_SLTL(context, *dag, negative_Sample_String, "negative", variables_Constants, terms));

	number_Of_Variables = positive_Sample->get_Number_Of_Variables();
	dag->set_Number_Of_Variables(number_Of_Variables);
}



Formula_SLTL::~Formula_SLTL()
{
}

Node* Formula_SLTL::build_Tree(z3::model &model, int root, Node** node_Vector, std::vector<bool>& touched) {

	for (int i = 0; i < number_Of_Variables; i++) {
		terms[i].print_Term(model, variables_Constants);
	}

	return Formula::build_Tree(model, root, node_Vector, touched);
}

std::string Formula_SLTL::print_Tree(Node * root)
{
	if (root->formula < number_Of_Variables) {
		return terms[root->formula].formula;
	}
	else {
		return Formula::print_Tree(root);
	}
}
