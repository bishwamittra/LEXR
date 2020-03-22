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

#include "Header/Formula.h"
#include "Header/Term_SLTL.h"

class Formula_SLTL :
	public Formula
{
public:
	Formula_SLTL(std::vector<std::string>& positive_Sample_String,
		std::vector<std::string>& negative_Sample_String,
		std::vector<std::string>& term_String);



	/*
	The Constant Variables used in the terms
	*/
	z3::expr_vector variables_Constants;

	~Formula_SLTL();

protected:


	std::vector<Term_SLTL> terms;



	Node* build_Tree(z3::model &model, int root, Node** node_Vector, std::vector<bool>& touched);
	std::string print_Tree(Node *root);


};

