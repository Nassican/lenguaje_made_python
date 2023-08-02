from unittest import TestCase
from lpp.ast import (
    Identifier,
    LetStatement,
    Program,
    ReturnStatement,
    Expression,
    ExpressionStatement
)
from lpp.lexer import Lexer
from lpp.parser import Parser
from typing import cast

# Para hacer los tests

# Generamos nuestro programa como un nodo del ast

class ParserTest(TestCase):

    def test_parse_program(self) -> None:
        source: str = 'variable x = 5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        # Verificar que hay "algo" dentro del programa
        self.assertIsNotNone(program)
        # Verificar que el programa es del tipo programa
        self.assertIsInstance(program, Program)

    def test_let_statement(self) -> None:
        source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self.assertEqual(len(program.statements), 3)

        for statement in program.statements:
            self.assertEqual(statement.token_literal(), 'variable')
            self.assertIsInstance(statement, LetStatement)

    def test_names_in_let_statements(self) -> None:
        source: str = '''
            variable x = 5;
            variable y = 10;
            variable foo = 20;
        '''
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        names: list[str] = []
        for statement in program.statements:
            # el cast es para que el test sepa LetStatement sea literalmente un statement
            statement = cast(LetStatement, statement) 
            assert statement.name is not None
            names.append(statement.name.value)

        expected_names: list[str] = ['x', 'y', 'foo']

        self.assertEquals(names, expected_names)

    def test_parse_errors(self) -> None:
        source: str = 'variable x 5;'

        lexer: Lexer = Lexer(source) # No le importa la gramatica
        parser: Parser = Parser(lexer) # Si le importa la gramatica

        program: Program = parser.parse_program()

        self.assertEquals(len(parser.errors), 1)

    def test_return_statement(self) -> None:
        source: str = '''
            retorna 5;
            retorna foo;
        '''

        lexer: Lexer = Lexer(source) # No le importa la gramatica
        parser: Parser = Parser(lexer) # Si le importa la gramatica

        program: Program = parser.parse_program()

        self.assertEquals(len(program.statements), 2)

        for statement in program.statements:
            self.assertEquals(statement.token_literal(), 'retorna')
            self.assertIsInstance(statement, ReturnStatement)

    def test_identifier_expression(self) -> None:
        source: str = 'foobar;'
        lexer: Lexer = Lexer(source) # No le importa la gramatica
        parser: Parser = Parser(lexer) # Si le importa la gramatica

        program: Program = parser.parse_program()

        # Funcion Auxiliar que dice los errores
        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        
        self._test_literal_expression(expression_statement.expression, 'foobar')

    def _test_program_statements(self,
                                 parser: Parser,
                                 program: Program,
                                 expected_statement_count: int = 1) -> None:
        self.assertEquals(len(parser.errors), 0)
        self.assertEquals(len(program.statements), expected_statement_count)
        self.assertIsInstance(program.statements[0], ExpressionStatement)

    def _test_literal_expression(self,
                                 expression: Expression,
                                 expected_value: any) -> None:
        value_type: type = type(expected_value)

        if value_type == str:
            self._test_identifier(expression, expected_value)
        else:
            self.fail(f'Tipo de expresión no controlada. Obtuvo={value_type}')

    def _test_identifier(self,
                         expression: Expression,
                         expected_value: str) -> None:
        self.assertIsInstance(expression, Identifier)
        identifier = cast(Identifier, expression)
        self.assertEquals(identifier.value, expected_value)
        self.assertEquals(identifier.token.literal, expected_value)
