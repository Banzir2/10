"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

import JackTokenizer


class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_stream: "JackTokenizer", output_stream: typing.TextIO) -> None:
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.output_stream = output_stream
        self.input_stream = input_stream
        self.indents = 0
        pass

    def print_indents(self):
        for i in range(self.indents):
            self.output_stream.write('\t')

    def print_type(self):
        if self.input_stream.token_type == 'keyword':
            self.print_keyword()
        else:
            self.print_identifier()

    def compile_class(self) -> None:
        """Compiles a complete class."""
        # Your code goes here!
        self.print_start('class')

        self.print_keyword()
        self.print_identifier()
        self.print_symbol()

        self.compile_class_var_dec()
        while self.input_stream.keyword() == 'function' \
                or self.input_stream.keyword() == 'method' \
                or self.input_stream.keyword() == 'constructor':
            self.compile_subroutine()

        self.print_symbol()
        self.print_identifier()

        self.print_end('class')
        pass

    def compile_class_var_dec(self) -> None:
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        self.print_start('classVarDec')

        while self.input_stream.keyword() == 'static' or self.input_stream.keyword() == 'field':
            self.print_vars()

        self.print_end('classVarDec')
        pass

    def print_vars(self):
        self.print_keyword()
        self.print_type()
        self.print_identifier()
        while self.input_stream.symbol() != ';':
            self.print_symbol()
            self.print_identifier()

    def compile_subroutine(self) -> None:
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        self.print_start('subroutineDec')

        self.print_keyword()
        self.print_type()
        self.print_identifier()
        self.print_symbol()
        self.compile_parameter_list()
        self.print_symbol()

        self.print_start('subroutineBody')
        self.print_symbol()
        self.compile_var_dec()
        self.compile_statements()
        self.print_symbol()
        self.print_end('subroutineBody')

        self.print_end('subroutineDec')
        pass

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        self.print_start('parameterList')
        while self.input_stream.token_type is not 'symbol':
            self.print_type()
            self.print_identifier()
            self.print_symbol()
        self.print_end('parameterList')
        pass

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        # Your code goes here!
        while self.input_stream.keyword() == 'var':
            self.print_start('varDec')
            self.print_vars()
            self.print_end('varDec')
        pass

    def is_statement(self) -> bool:
        return self.input_stream.keyword() == 'if' \
            or self.input_stream.keyword() == 'while' \
            or self.input_stream.keyword() == 'let' \
            or self.input_stream.keyword() == 'do' \
            or self.input_stream.keyword() == 'return'

    def compile_statements(self) -> None:
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        while self.is_statement():
            if self.input_stream.keyword() == 'while':
                self.compile_while()
            if self.input_stream.keyword() == 'let':
                self.compile_let()
            if self.input_stream.keyword() == 'do':
                self.compile_do()
            if self.input_stream.keyword() == 'return':
                self.compile_return()
            if self.input_stream.keyword() == 'if':
                self.compile_if()
        pass

    def compile_subroutine_call(self) -> None:
        if self.input_stream.symbol() == '(':
            self.print_symbol()
            self.compile_expression_list()
            self.print_symbol()
            return
        if self.input_stream.symbol() == '.':
            self.print_symbol()
            self.print_identifier()
            self.compile_subroutine_call()
            return
        pass

    def compile_do(self) -> None:
        """Compiles a do statement."""
        # Your code goes here!
        self.print_start('doStatement')
        self.print_keyword()
        self.print_identifier()
        self.print_symbol()
        self.compile_subroutine_call()
        self.print_symbol()
        self.print_end('doStatement')
        pass

    def compile_let(self) -> None:
        """Compiles a let statement."""
        # Your code goes here!
        self.print_start('letStatement')
        self.print_keyword()
        self.print_identifier()
        if self.input_stream.symbol() == '[':
            self.print_symbol()
            self.compile_expression()
            self.print_symbol()
        self.print_symbol()
        self.compile_expression()
        self.print_symbol()
        self.print_end('letStatement')
        pass

    def compile_while(self) -> None:
        """Compiles a while statement."""
        # Your code goes here!
        self.print_start('whileStatement')
        self.print_keyword()
        self.print_symbol()
        self.compile_expression()
        self.print_symbol()
        self.print_symbol()
        self.compile_statements()
        self.print_symbol()
        self.print_end('whileStatement')
        pass

    def compile_return(self) -> None:
        """Compiles a return statement."""
        # Your code goes here!
        self.print_start('returnStatement')
        self.print_keyword()
        if self.input_stream.token_type == 'symbol':
            self.print_symbol()
            return
        self.compile_expression()
        self.print_symbol()
        self.print_end('returnStatement')
        pass

    def compile_if(self) -> None:
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        self.print_start('ifStatement')
        self.print_keyword()
        self.print_symbol()
        self.compile_expression()
        self.print_symbol()
        self.print_symbol()
        self.compile_statements()
        self.print_symbol()
        if self.input_stream.keyword() == 'else':
            self.print_keyword()
            self.print_symbol()
            self.compile_statements()
            self.print_symbol()
        self.print_end('ifStatement')
        pass

    def is_op(self):
        return self.input_stream.symbol() in\
            ['+', '-', '*', '/', '&', '|', '<', '>', '=', '~', '^', '#']

    def compile_expression(self) -> None:
        """Compiles an expression."""
        # Your code goes here!
        self.compile_term()
        while self.is_op():
            self.print_symbol()
            self.compile_term()
        pass

    def compile_term(self) -> None:
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        self.print_start('term')
        if self.input_stream.token_type() == 'symbol':
            if self.input_stream.symbol() == '(':
                self.print_symbol()
                self.compile_expression()
                self.print_symbol()
                return
            elif self.input_stream.symbol() in ['-', '~', '#', '^']:
                self.print_symbol()
                self.compile_term()
        if self.input_stream.token_type() == 'identifier':
            self.print_identifier()
            if self.input_stream.symbol() == '[':
                self.print_symbol()
                self.compile_expression()
                self.print_symbol()
            if self.input_stream.symbol() == '(' or self.input_stream.symbol() == '.':
                self.compile_subroutine_call()
            return
        if self.input_stream.token_type() == 'int_const':
            self.print_int()
        self.print_end('term')
        pass

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        self.print_start('expressionList')
        if self.input_stream.symbol() is not ')':
            self.compile_expression()
        while self.input_stream.symbol() is not ')':
            self.print_symbol()
            self.compile_expression()
        self.print_end('expressionList')
        pass

    def print_keyword(self):
        self.print_indents()
        self.output_stream.write(f'<keyword> {self.input_stream.keyword()} </keyword>\n')
        self.input_stream.advance()

    def print_identifier(self):
        self.print_indents()
        self.output_stream.write(f'<identifier> {self.input_stream.identifier()} </identifier>\n')
        self.input_stream.advance()

    def print_symbol(self):
        self.print_indents()
        self.output_stream.write(f'<symbol> {self.input_stream.symbol()} </symbol>\n')
        self.input_stream.advance()

    def print_int(self):
        self.print_indents()
        self.output_stream.write(f'<Int.Const.> {self.input_stream.int_val()} </Int.Const.>\n')
        self.input_stream.advance()

    def print_start(self, word: str):
        self.print_indents()
        self.output_stream.write(f'<{word}>\n')
        self.indents += 1

    def print_end(self, word: str):
        self.indents -= 1
        self.print_indents()
        self.output_stream.write(f'</{word}>\n')
