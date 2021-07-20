**OLL Language Specifications**

**Version 1.00**

**Purpose of the Document:**

This document summarizes the features supported by the OLL. For each group of features, implementation success criteria is split into &#39;threshold&#39; and &#39;objective&#39; levels. Threshold is the minimum acceptable implementation level and Objective is the desired implementation level.

**General Design Consideration**

OLL syntax is similar to the C and JavaScript family of languages. Blocks of code are designated by curly braces {}. Whitespace and newline characters are generally ignored. Each statement must end with the semicolon character. Execution starts from the beginning of the file.

**Memory Management**

Threshold: Memory is automatically allocated for new variables and objects, but is not automatically freed when the objects are no longer in use.

Objective: Memory is managed automatically. Allocated when the new variables / objects are created and garbage collected when such objects are no longer used / referenced in the code.

**Comments**

Threshold: Comments start with // token. All code from // until the new line character is ignored.

Objective: Support multi-line comment blocks. Those start with the /\* token and end with the \*/ token.

**Variables**

Threshold: Variable names can consist of capital and lowercase letters, digits and underscores. Variable names can only start with either a letter or an underscore. OLL supports variable names of any length.

Variables must be declared before they are used. Declaration is done with the var keyword. Declaration can only be done once within applicable scope. When the variable is declared but not yet assigned any value, its type is integer and the value is 0.

Variables can store any types of values supported by the OLC. Types of value stored in the particular variable can change during the execution of the program. When several variables are used in the expression, no implicit casting is done. Variable types must be the same or the error will be reported.

**Variable Types**

Threshold: OLL support one primitive data type - SIGNED INT32. When used in the conditional expressions, integer values of 0 will evaluate to False and anything will evaluate to True.

Objective: Support for boolean values, NULL, strings,Float and References (pointers) to the objects created from classes, as well as to the arrays.

**Data Structures**

Threshold: no built-in data structures are supported.

Objective: OLL supports StaticArray that can store variables of any type. Size of the array is specified when it is declared and does not change after that. Array supports standard operations by getting / setting the value of the element given its index.

**Scope of the variables**

Threshold: OLL supports global variables. They are declared anywhere in the file.

Objective: Support block-scoped variables. Variables declared inside blocks designed with the curly braces are only accessible within that block of code. If this stretch goal is achieved, global variables will be those declared outside of any functions of classes.

**Control Structures**

Threshold: OLC supports two primary control structures - if-else statement and a while loop. The syntax is as follows:

    if (condition) {

        // some code

        } else {

        // some other code

      }

    while (condition) {

        // some code

    }

Objective: Support if-elif-else, for-loop, while-else loops.

**Operators:**

Threshold: Built-in int32 data type supports the following arithmetic operators: add, sub, mul, div, mod. Also, the following boolean operations: not, and, or.

Objective: Boolean operators also support xor. All of the above operators should have a way of working on all variable types, including pointers.

**Functions:**

Threshold: Functions are declared by using function () { }. Functions always return a value. If there\'s no return statement inside the function, it implicitly returns 0. Functions only support positional parameters. Parameters only exist within the scope of the function and are garbage collected when it returns.

Objective: Same as the Threshold

**Classes**

Threshold: No support for classes.

Objective: Basic classes are supported. Classe are declared using the keyword class, followed by the name of the class. Inheritance is not supported. All functions and variables declared within the class are instance variables and methods. OLL does not support static methods or variables. init() method, if declared inside the class is treated as a constructor.

**Input-output operators:**

Threshold: Support putchar operator. It takes an integer value (in the range from 0-255) and outputs an ascii character corresponding to this value to the standard output.

Objective: Built-in print operator displays the value of any primitive data type supported by the language.
