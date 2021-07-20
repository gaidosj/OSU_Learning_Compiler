**Introduction**

Our team will be completing a compiler for a new programming language that we are creating.  Individually, we have never taken a formal course in compilers or computation.  However, we think such a project would be an ideal way to combine all the different topics we have learned at Oregon State University into a single deliverable.

**User Perspective**

Users new to compilers will find the field to be large and complex.  We would like to simplify their first exposure and make it easier for learners to see the different parts in action.  The OSU Learning Language, hereafter called OLL, is a simple language with a small learning curve.  The source code should be reminiscent of C and therefore familiar to many developers.  Each part of the compilation process will have a distinct component available for dissection and study with sample inputs and outputs.  Each stage, as well as the overall project, will be well-documented.  

**Client**

Our instructor and the teaching assistant will be considered our clients for this project.  The client requirements will be those listed in this document, the syllabus, and any approved changes to the documentation that may occur over the term.

**Software Structure**

A compiler is composed of a front-end, a middle-end, and a back-end.  The middle-end is focused on optimization and is outside the scope of this project.  The majority of our work will target the front-end:  taking the source code of a language into an abstract syntax tree.  The back-end will be addressed sufficiently to have programs execute but will not be fully built out with our own code.  

The OLL will be compiled using the OSU Learning Compiler (OLC). Based on our preliminary research to this point, it is typical to break down the implementation of a new language and related compiler into the following modules:

1.  Lexer module - that would scan the original source code and convert it to a list of tokens. It would also report any error condition when detecting some invalid tokens.

2.  Parser module - taking as input a list of tokens produced by the lexer, this module will build an abstract syntax tree representation (AST) of the source code. It will also detect and report any syntax errors.

3.  Transpiler module - using AST code representation, produces equivalent source code in some common programming language. Such transpiled code could be compiled / executed using the tools / runtime associated with the target language. Our goal is to transpile to a high-level language that has support for classes and automatic memory management. Current considerations are Python or JavaScript.

**Libraries, Languages, APIs, and Development Tools**

Python 3.8.1 will be our primary language for this project, with the built-in unittest library for writing tests. We like Python for this project because we're all familiar with the language and it will allow us to iterate quickly during the accelerated quarter.

We discussed using third-party tools such as Flex to generate the lexer and Bison to generate the parser.  However, we believe there will be a better learning experience to build a hands-on implementation from scratch. Currently. we don't have any intention of using third-party tools or APIs.  We anticipate this may change for building out the back-end of the compiler if the requirements flex due to time constraints.  

The project will be linted using Flake8 and maintained with Continuous Integration via GitHub Actions, mandatory code review, and branch protection on the main branch.