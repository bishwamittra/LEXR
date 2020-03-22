# flie - The Formal Language Inference Engine

flie offers various (syntax-guided) algorithms for learning descriptive (formal) languges from classified strings.

Currently, flie supports two languages (with more to come):
- Linear Temporal Logic (LTL)
- A restricted version of Signal Temporal Logic (SLTL), currently without time-constraints on the temporal modalities

flie can operate in two modes:
1. Generating fully consistent models (i.e., formulas that classify all strings correctly)
2. Generating semi consistent models (i.e., formulas up to a given size correctly classifying as many strings as possible)

For some formal languages, the user can restrict the search space for possible solutions using context-free grammars (see details below).
The following table gives a detailed overview over flie's features. 

|      | Fully consistent | Fully consistent + syntax-guided | Semi consistent | Semi consistent + syntax-guided |
|------|------------------|----------------------------------|-----------------|---------------------------------| 
| LTL  | Yes              | Yes                              | Yes             | Yes                             |
| SLTL | Yes              | No                               | Yes             | No                              |


# Building flie

In the following, we assume a Linux-based operating system, such as Ubuntu. We
have also tested flie on Windows but do not provide instructions for it.

## Requirements

Apart from the usual GNU compiler collection (which is likely to be pre-installed
on any Linux distribution), flie requires one external library:
- [Microsoft Z3](https://github.com/Z3Prover/z3) >= 4.8.0

This README assumes that Z3 is installed on your system. If this is not the case,
follow the instructions on the Z3 Github page to install it. (We later also
describe a method to compile flie if you cannot install Z3 on your system.)

## Compilation

To compile flie, just execute the following command in the root folder of flie:

```shell
    make
```

This will generate a binary named `flie` (or `flie.exe` on Windows) in the same
directory.

Should have Z3 not installed on your machine, you can specify where the build
utility searches for the headers and library files. To this end, set the
following two environment variables:
- `Z3_INCLUDE` points to where the headers are located
- `Z3_LIB` points to where the library file (i.e., `libz3.so`) is located

You can also prefix the call to the make utility with these environment variables:

```shell
    Z3_INCLUDE=<path-to-Z3-includes> Z3_LIB=<path-to-libz3.so> make
```


# Running flie 

To run flie, just execute the binary `flie` (respectively `flie.exe` on Windows):

```shell
    ./flie
```

Without arguments, flie will display a help text.

Should Z3 not be installed on your system, you need to let the environment
variable `LD_LIBRARY_PATH` point to the folder the file `libz3.so` is located.
Again, you can can prefix the call to flie with this environment variable:

```shell
    LD_LIBRARY_PATH=<path-to-libz3.so> ./flie
```

Note that Windows uses the `PATH` environment variable instead.





# Problem Descriptions

The problem which is solved by the program takes two sets of words as input. These two input sets will be called **sample**. If a formula has the following two properties it is called **consistent** with the sample:
1. All the words in the first set of the sample are a model for the formula.
2. All the words in the second set of the sample are no model for the formula.

For a specific sample the program now generates a single formula consistent with the input sample.

## LTL

In this case the input sample consists of two sets of ultimately period words. The letters of the words a vectors of binary variables. The output of the program will be a LTL formula consistent with the input set.

## SLTL

In contrast to LTL a model for a SLTL formula is not a word of vectors of binary variables but rather a word of vectors of rational variables called signals. An example input sample with two signals could be:
Words that are a model for the output formula:

>{(0.1, 0.2)(0.3,0)\*, (0.2,1.5)(4.7,3.0)\*}

Words that are no model for the output formula:
>{(0.3, 0.1)(0.3,1.0)\*, (0.7,1.2)(0.7,4.2)\*}

A SLTL formula is a restriction of a STL formula. In addition to propositional and LTL operators mathematical operators can be used to create terms. These terms can be constructed by using other terms, signals or constants. To be used by the other operators the terms have to be combined with an comparative operator (e.g. <, >). A formula solving the example input could be F(G(s0 > s1)), a shorter formula could be s0 < c with the constant c being 0.25.

Additionally to sample, there is another input. In order to reduce complexity a set of terms is input as well. Each of the terms will output a boolean value (e.g. s0 + s1 < c0). These terms are the only terms which can be used inside the SLTL formula.


## Using Context Free Grammar

If one wants to further constrain the output formula, a context free grammar can be used. The language of the grammar should contain all formulas which can be a suitable solution for your problem. Furthermore the context free grammar has to generate exactly one operator or variable with each derivation. An example of such a grammar could be:
```
N0 -> F(N1)
N1 -> (N1) && (N1) | (N1) || (N1) | (N1) => (N1) | (N1) U (N1) | F(N1) | !(N1) | G(N1) | X (N1) | x0
```


This grammar would constrain the output formula to start with a Finally operator.

## Optimizing

As it is unclear at the beginning how big the resulting formula is, a maximal size (*max*) can be input. If this option is chosen the program continues to compute the smallest formula consistent with the input sample. In contrast to the base program this will end if the formula would get bigger than *max*. The program then outputs a formula the size of *max* which classifies the maximal number of words in the input sample.

# Command Line Arguments

Here i will explain which command line arguments can be used to solve the various problems described in the previous section. Without any arguments the program will output a help text. 

|Argument        |Meaning                      
|----------------|------------------------------
|-f \<path>| Specifies the path to a single trace file which should be examined. If no further argument is given, the program will solve the [LTL problem](#ltl).                
|-max \<iteration>|Specifies the maximal size a formula should take. If this argument is specified the [optimizing](#optimizing) problem will be solved. This argument can be used in both the [LTL](#ltl) and [SLTL](#sltl) case.
|-g | Specifies whether a grammar like in section [CFG](#using-context-free-grammar) is used to constrain the output formulas. This option can only be used in the [LTL](#ltl) case. 
|-sltl| This is used if the  [SLTL problem](#sltl) should be solved instead of the [LTL problem](#ltl).
|-v| Outputs the computation time at the end of the program.
|-vv| Outputs the computation time at the end of the program as well as the start of each iteration of the algorithm.
|-h| Outputs the help.
	

# Trace File Format:

## LTL-Trace File:

Example file:
	
	1,0;1,1::0
	---
	1,0;0,1::0
	0,1;1,0::1
	1,0;0,0::1
	---
	part 3
	---
	part 4
	---
	N0>||,N1,N1;X,N1
	N1>&&,N1,N1;x0;x1

An LTL-file consists of 4 parts (5 parts if a grammar is used). Each of these parts is separated by a line containing only "\-\-\-"
	
**First part:** Represents the traces which should be accepted. In each line there is exactly one trace. The example file only has one accepting trace.

**Second part:** Represents the traces which should be rejected. In each line there is exactly one trace. The example file has three rejecting traces.

**Third part:** Consists of the operators that the program should use. This is not yet implemented and therefore the content of this line is irrelevant.

**Fourth part:** Contains the maximal depth which should be explored. This is not yet implemented and therefore the content of this line is irrelevant.

**Fifth part:**  Consists of the production rules of a grammar, this part can be omitted if no grammar is used.
	
### Traces:

A single trace consists of the values of all variables in the different time steps.
>1,0;0,1;1,1::2 

This an example of a trace line consisting of two variables. The values of these variables are:
> x0: 1,0,1*
	x1: 0,1,1*

The integer after "::" is the time steps from where the values will repeat.

### Grammar:

The grammar has to use the Nonterminals *N0...Nn* if *n+1* Nonterminals are used. The i-th line will consist of the production rules where	*Ni* is on the left side. The production rules are separated by semicolons.

> N5>||,N1,N3;X,N2;x0

This example represents the production rules: *N5 &rarr; ||(N1,N3)* , *N5 &rarr; X(N2)* and *N5 &rarr; x0*
	
In the example file the solution without using the grammar would be *G(x0)*. If the grammar is used, the solution is *X(&&(x0,x1))*.
	
	

## SLTL-Trace Files:

Example file:
		
	2.0,1.0::0
	---
	1.0,1.0::0
	2.0,2.0::0
	1.0,2.0::0
	---
	part 3
	---
	part 4
	---
	=(s0,c0)
	<(+(s1,s0),c1)

An SLTL-file consists of 5 parts. Each of these parts is separated by the line "\-\-\-"
	
**First part:** Represents the traces which should be accepted. In each line there is exactly one trace. The example file only has one accepting trace.

**Second part:**	Represents the traces which should be rejected. In each line there is exactly one trace. The example file has three rejecting traces.

**Third part:**	Consists of the operators that the program should use. This is not yet implemented and therefore the content of this line is irrelevant.

**Fourth part:** Contains the maximal depth which should be explored. This is not yet implemented and therefore the content of this line is irrelevant.

**Fifth part:** Consists of the terms which can be used by the program.

### Traces:

A single trace line consists of the values of all variables in different time steps.
>1.0,0.2;0.1,1.3;1.6,1.0::2 

This an example of a trace line consisting of two variables. The values of these variables are:

> x0: 1.0,0.1,(1.6)*
		x1: 0.2,1.3,(1.0)*

The integer after "::" is the time steps from where the values will repeat.
		
### Terms:

In part 5 there is a single Term is added in each line. The constants *c0...cn* can be used if *n+1* constants are used overall. The operators that can be used in the terms are *{<,>,=,!(not equal),+,-,\*}* after each of the operators the input has to be written inside of brackets separated by ",".
	
In the example file a solution would be *(s0=c0)&&(s1+s0 < c1)* with *c0 = 2.0* and *c1 = 4.0*.
