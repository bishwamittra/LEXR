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
#include "Header/Term_SLTL.h"

class Sample_Tracer_SLTL :
	public Sample_Tracer
{
public:
	Sample_Tracer_SLTL(z3::context& context,
		Dag& dag,
		std::vector<std::string>& sample_String,
		std::string sample_Name,
		z3::expr_vector& variables_Constants,
		std::vector<Term_SLTL>& terms);

	~Sample_Tracer_SLTL();

	void initialize();

protected:

	std::vector<std::pair<std::vector<std::vector<std::string> >, int> > sample;


	std::vector<Term_SLTL>& terms;
	z3::expr_vector& variables_Constants;

	void add_Formulas_Atomic(int iteration);

	void create_Sample(std::vector<std::string> input_Sample_SLTL);



};

