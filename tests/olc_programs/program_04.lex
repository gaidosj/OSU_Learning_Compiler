COMMENT '// DEMO PROGRAM FOR OSU LEARNING COMPILER PROJECT'; EOL
COMMENT '// This program demonstrates implementation of:'; EOL
COMMENT '// - built-in sttements (print)'; EOL
COMMENT '// - variables (lexically scoped) of int, string and function types'; EOL
COMMENT '// - flow control, using if statements and loops'; EOL
COMMENT '// - functions (as first-class citizens)'; EOL
EOL
FUNCTION 'function'; IDENTIFIER 'fib'; LEFT_PAREN '('; IDENTIFIER 'n'; RIGHT_PAREN ')'; LEFT_CURLY '{'; EOL
COMMENT '// Function to return N-th Fibonacci number'; EOL
EOL
IF 'if'; LEFT_PAREN '('; IDENTIFIER 'n'; LT '<'; INT '0' val=0; RIGHT_PAREN ')'; RETURN 'return'; STRING ''THERE IS NO NEGATIVE FIBONACCI NUMBER'' val=THERE IS NO NEGATIVE FIBONACCI NUMBER; SEMICOLON ';'; EOL
IF 'if'; LEFT_PAREN '('; IDENTIFIER 'n'; LT '<'; INT '2' val=2; RIGHT_PAREN ')'; RETURN 'return'; IDENTIFIER 'n'; SEMICOLON ';'; EOL
EOL
VAR 'var'; IDENTIFIER 'first_number'; EQUALS '='; INT '0' val=0; SEMICOLON ';'; EOL
VAR 'var'; IDENTIFIER 'second_number'; EQUALS '='; INT '1' val=1; SEMICOLON ';'; EOL
VAR 'var'; IDENTIFIER 'third_number'; EQUALS '='; INT '0' val=0; SEMICOLON ';'; EOL
VAR 'var'; IDENTIFIER 'counter'; EQUALS '='; INT '0' val=0; SEMICOLON ';'; EOL
EOL
WHILE 'while'; LEFT_PAREN '('; IDENTIFIER 'counter'; PLUS '+'; INT '1' val=1; LT '<'; IDENTIFIER 'n'; RIGHT_PAREN ')'; LEFT_CURLY '{'; EOL
IDENTIFIER 'third_number'; EQUALS '='; IDENTIFIER 'first_number'; PLUS '+'; IDENTIFIER 'second_number'; SEMICOLON ';'; EOL
IDENTIFIER 'first_number'; EQUALS '='; IDENTIFIER 'second_number'; SEMICOLON ';'; EOL
IDENTIFIER 'second_number'; EQUALS '='; IDENTIFIER 'third_number'; SEMICOLON ';'; EOL
IDENTIFIER 'counter'; EQUALS '='; IDENTIFIER 'counter'; PLUS '+'; INT '1' val=1; SEMICOLON ';'; EOL
RIGHT_CURLY '}'; EOL
RETURN 'return'; IDENTIFIER 'third_number'; SEMICOLON ';'; EOL
RIGHT_CURLY '}'; EOL
EOL
FUNCTION 'function'; IDENTIFIER 'generic_compute_function'; LEFT_PAREN '('; RIGHT_PAREN ')'; LEFT_CURLY '{'; EOL
COMMENT '// Functions can be returned as values'; EOL
RETURN 'return'; IDENTIFIER 'fib'; SEMICOLON ';'; EOL
RIGHT_CURLY '}'; EOL
EOL
VAR 'var'; IDENTIFIER 'fib_index'; EQUALS '='; MINUS '-'; INT '1' val=1; SEMICOLON ';'; EOL
VAR 'var'; IDENTIFIER 'fib_function'; EQUALS '='; IDENTIFIER 'generic_compute_function'; LEFT_PAREN '('; RIGHT_PAREN ')'; SEMICOLON ';'; EOL
EOL
WHILE 'while'; LEFT_PAREN '('; IDENTIFIER 'fib_index'; LT '<'; INT '24' val=24; RIGHT_PAREN ')'; LEFT_CURLY '{'; EOL
PRINT 'print'; IDENTIFIER 'fib_function'; LEFT_PAREN '('; IDENTIFIER 'fib_index'; RIGHT_PAREN ')'; SEMICOLON ';'; EOL
IDENTIFIER 'fib_index'; EQUALS '='; IDENTIFIER 'fib_index'; PLUS '+'; INT '3' val=3; SEMICOLON ';'; EOL
RIGHT_CURLY '}'; EOL
EOF