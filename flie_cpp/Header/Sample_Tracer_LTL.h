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
#include "Header/Sample_Tracer.h"
#include <z3++.h>

class Sample_Tracer_LTL :
	public Sample_Tracer
{
public:

	

	/*
	Is a vector containing all words of the sample. A word is given by a tuple.
	The first part is the letters of the word consisting of a bool for each variable of the letter.
	The second part is the index of the position in the word from where it repeats.
	*/
	std::vector<std::pair<std::vector<std::vector<bool> >, int> > sample;

	/*
	Constructor used when a new solver is created in each iteration.
	context: the context where all expressions are added
	number_Of_Variables: the number of variables each letter of each word consists of
	dag: formulas and variables used to represent the DAG
	sample: vector of all the words in the sample
	sample_Name: either positive or negative, depending on wether the words in the sample should be satisfied or not
	*/
	Sample_Tracer_LTL(z3::context& context, Dag& dag,
		std::vector<std::string>& sample,
		std::string sample_Name);

	~Sample_Tracer_LTL();


	void initialize();
	void add_Formulas_Atomic(int iteration);
	void add_Formulas(int iteration);

protected:

	void create_Sample(std::vector<std::string> input_Sample_LTL);
	
};

