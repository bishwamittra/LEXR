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

#include "Header/Formula_LTL.h"
#include "Header/Sample_Tracer_LTL.h"




Formula_LTL::Formula_LTL(std::vector<std::string>& positive_Sample_String,
	std::vector<std::string>& negative_Sample_String)
{

	start = clock();

	dag = std::unique_ptr<Dag>(new Dag(context));
	positive_Sample = std::unique_ptr<Sample_Tracer>(new Sample_Tracer_LTL(context, *dag, positive_Sample_String, "positive"));
	negative_Sample = std::unique_ptr<Sample_Tracer>(new Sample_Tracer_LTL(context, *dag, negative_Sample_String, "negative"));

	number_Of_Variables = positive_Sample->get_Number_Of_Variables();
	dag->set_Number_Of_Variables(number_Of_Variables);
}



Formula_LTL::~Formula_LTL()
{
}


std::string Formula_LTL::print_Tree(Node * root)
{
	if (root->formula < number_Of_Variables) {
		std::stringstream result;
		result << "x";
		result << (root->formula);
		return result.str();
	}
	else {
		return Formula::print_Tree(root);
	}
}




