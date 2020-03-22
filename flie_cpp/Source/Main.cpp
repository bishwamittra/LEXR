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



#include <vector>
#include <fstream>
#include <string.h>
#include "Header/Formula.h"
#include "Header/Formula_LTL.h"
#include "Header/Formula_SLTL.h"

/*
Splits an LTL file into vectors of strings containing the different sections of the file:
	0 all words which should be satisfied
	1 all words which should not be satisfied
	2 a single string containing all usable operators
	3 a single string containing the maximal depth
	4 the grammar if one is used

	input: the path to the input file
*/
std::vector<std::vector<std::string> > split_Input_LTL(char* input) {

	std::ifstream input_File(input);
	std::string line;
	std::vector<std::vector<std::string> > result;


	//read in file

	std::vector<std::string> positive_Sample_Input;
	std::vector<std::string> negative_Sample_Input;
	std::vector<std::string> usable_Operators;
	std::vector<std::string> depth;
	std::vector<std::string> grammar;


	if (input_File.is_open()) {

		//get positive sample

		while (std::getline(input_File, line) && line.compare("---")) {
			positive_Sample_Input.push_back(line);
		}

		//get negative sample

		while (std::getline(input_File, line) && line.compare("---")) {
			negative_Sample_Input.push_back(line);
		}

		//get set of usable formulas

		std::getline(input_File, line);

		std::getline(input_File, line); // skipping next ---

		//get depth

		std::getline(input_File, line);
		depth.push_back(line);

		std::getline(input_File, line); // skipping next ---

		//get grammar if possible
		
		while (std::getline(input_File, line) && line.compare("---")) {
			grammar.push_back(line);
		}

		input_File.close();

		result.push_back(positive_Sample_Input);
		result.push_back(negative_Sample_Input);
		result.push_back(usable_Operators);
		result.push_back(depth);
		result.push_back(grammar);
		

	}
	else {
		std::cout << input << std::endl;
		std::cout << "unable to open file" << std::endl;
	}

	return result;
}

/*
Splits an SLTL file into vectors of strings containing the different sections of the file:
	0 all words which should be satisfied
	1 all words which should not be satisfied
	2 a single string containing all usable operators
	3 a single string containing the maximal depth
	4 the terms which can be used 
	5 the grammar if one is used

	input: the path to the input file
*/
std::vector<std::vector<std::string> > split_Input_SLTL(char* input) {

	std::ifstream input_File(input);
	std::string line;
	std::vector<std::vector<std::string> > result;

	//read in file

	std::vector<std::string> positive_Sample_Input;
	std::vector<std::string> negative_Sample_Input;
	std::vector<std::string> usable_Operators;
	std::vector<std::string> depth;
	std::vector<std::string> input_Terms;
	std::vector<std::string> grammar;

	if (input_File.is_open()) {

		//get positive sample

		while (std::getline(input_File, line) && line.compare("---")) {
			positive_Sample_Input.push_back(line);
		}

		//get negative sample

		while (std::getline(input_File, line) && line.compare("---")) {
			negative_Sample_Input.push_back(line);
		}

		//get set of usable formulas

		std::getline(input_File, line);

		std::getline(input_File, line); // skipping next ---

		//get depth

		std::getline(input_File, line);
		depth.push_back(line);

		std::getline(input_File, line); // skipping next ---

		//get set of usable formulas
		while (std::getline(input_File, line) && line.compare("---")) {
			input_Terms.push_back(line);
		}

		//get grammar if possible

		while (std::getline(input_File, line) && line.compare("---")) {
			grammar.push_back(line);
		}

		input_File.close();

		result.push_back(positive_Sample_Input);
		result.push_back(negative_Sample_Input);
		result.push_back(usable_Operators);
		result.push_back(depth);
		result.push_back(input_Terms);
		result.push_back(grammar);
	}
	else {
		std::cout << input << std::endl;
		std::cout << "unable to open file";
	}

	return result;
}

/*
Executes the algorithm for given parameters for a single input file.

	using_Grammar: is true if a grammar should be used in all files
	using_Incremental: is true if an incremental solver should be used in all files
	using_SLTL: is true if all files are SLTL files
	optimized_Run: gives the iteration in which max sat is used instead of sat
	input: the paths to the input file
*/
void solve_Single_File(bool using_Grammar, bool using_Incremental, bool using_SLTL, int optimized_Run, char * input, int verbose)
{
	Formula* formula;
	std::vector<std::vector<std::string> > input_Split;
	int grammar_Index;

	if (!using_SLTL) {

		input_Split = split_Input_LTL(input);
		if (input_Split.size() < 1) return;
		formula = new Formula_LTL(input_Split[0], input_Split[1]);
		grammar_Index = 4;
	}
	else {
		input_Split = split_Input_SLTL(input);
		if (input_Split.size() < 1) return;
		formula = new Formula_SLTL(input_Split[0], input_Split[1], input_Split[4]);
		grammar_Index = 5;
	}

	if (using_Grammar) {
		formula->set_Grammar(input_Split[grammar_Index]);
	}

	if (optimized_Run > 0) {
		formula->set_Optimized_Run(optimized_Run);
	}

	if (using_Incremental) {
		formula->set_Using_Incremental();
	}
	formula->set_Vebose(verbose);
	formula->initialize();
	formula->find_LTL();
}

/*
Executes the algorithm for given parameters for a set of inputs.

	using_Grammar: is true if a grammar should be used in all files
	using_Incremental: is true if an incremental solver should be used in all files
	using_SLTL: is true if all files are SLTL files
	optimized_Run: gives the iteration in which max sat is used instead of sat
	input_Files: a vector of paths to the input files
*/
void solve_Multiple_Files(bool using_Grammar, bool using_Incremental, bool using_SLTL, int optimized_Run, std::vector<char*> input_Files, int verbose) {


	std::ofstream myfile;
	myfile.open("results.txt");

	std::string result;
	for (char* file : input_Files) {
		clock_t start = clock();

		solve_Single_File(using_Grammar, using_Incremental, using_SLTL, optimized_Run, file, verbose);

		clock_t end = clock();


		myfile << result << "	";

		unsigned long time = (end - start);
		myfile << time << "\n";
	}
	myfile.close();

}

void print_Help() {
	std::cout << "Command Line Arguments:\n " << std::endl;
	std::cout << "-f <path>:	Specifies the path to a single trace file which should be examined.\n" << std::endl;
	std::cout << "-max <iteration>:	Specifies the iteration in which MAX-SAT solver is used instead of a SAT Solver. If this argument is not used MAX-SAT will not be used.\n" << std::endl;
	std::cout << "-i:	Specifies whether an incremental solver should be used.\n" << std::endl;
	std::cout << "-g:	Specifies whether a grammar is used to limit the output formulas.\n" << std::endl;
	std::cout << "-sltl:	Specifies whether the input file is a SLTL example.\n" << std::endl;
	std::cout << "Example Files can be found in the Trace directory and in the README file.\n" << std::endl;
}

int main(int argc, char* argv[]) {

	// Input Parameters:

	bool using_Grammar = false;
	bool using_Incremental = false;
	bool using_SLTL = false;
	int verbose = 0;
	int optimized_Run = 0;
	char* input = nullptr;
	std::vector<char*> input_Files;


	std::vector<std::string> strings;

	// setting the input parameters

	for (int i = 0; i < argc; i++) {
		if (!strcmp(argv[i], "-g")) using_Grammar = true;
		if (!strcmp(argv[i], "-i")) using_Incremental = true;
		if (!strcmp(argv[i], "-f")&& (i + 1) < argc) input = argv[i + 1];
		if (!strcmp(argv[i], "-max") && (i + 1) < argc) optimized_Run = std::stoi(argv[i + 1]);
		if (!strcmp(argv[i], "-sltl")) using_SLTL = true;
		if (!strcmp(argv[i], "-range") && (i + 2) < argc) {

			int initial_Number = std::stoi(argv[i + 1]);
			int last_Number = std::stoi(argv[i + 2]);

			for (int j = initial_Number; j <= last_Number; j++) {

				std::stringstream ss;
				if (j < 10) {
					ss << "traces/000";
				}
				else if (j < 100) {
					ss << "traces/00";
				}
				else if (j < 1000) {
					ss << "traces/0";
				}
				else {
					ss << "traces/";
				}
				ss << j;
				ss << ".trace";
				strings.push_back(ss.str());
				char* input_File = const_cast<char*> (strings.back().c_str());
				std::ifstream infile(input_File);
				if (infile.is_open()) {
					input_Files.push_back(input_File);
				}
				infile.close();
			}
		}
		if (!strcmp(argv[i], "-h") || argc  == 1) {
			print_Help();
			return 0;
		}
		if (!strcmp(argv[i], "-v")) verbose = 1;
		if (!strcmp(argv[i], "-vv")) verbose = 2;
	}


	if (input_Files.size() > 0) {

		// execute for all files in a range

		solve_Multiple_Files(using_Grammar, using_Incremental, using_SLTL, optimized_Run, input_Files, verbose);
	}
	else if(input){

		// execute for a single file

		solve_Single_File(using_Grammar, using_Incremental, using_SLTL, optimized_Run, input, verbose);
	}
	else {
		std::cout << "No input File\n" << std::endl;
		print_Help();
	}

	return 0;
}
