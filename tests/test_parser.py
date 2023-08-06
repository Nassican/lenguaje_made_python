from unittest import TestCase
from lpp.ast import (
    LetStatement,
    Program,
    ReturnStatement,
    Expression,
    ExpressionStatement,
    Identifier,
    Integer,
    Prefix,
    Infix,
    Boolean,
    If,
    Block,
    Function,
    Call
) 
from lpp.lexer import Lexer
from lpp.parser import Parser
from typing import (
    cast, 
    List, 
    Dict, 
    Tuple, 
    Type, 
    Any, 
    Optional,
    )

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

        lexer: Lexer = Lexer(source)  # No le importa la gramatica
        parser: Parser = Parser(lexer)  # Si le importa la gramatica

        program: Program = parser.parse_program()

        self.assertEquals(len(parser.errors), 1)

    def test_return_statement(self) -> None:
        source: str = '''
            retorna 5;
            retorna foo;
        '''

        lexer: Lexer = Lexer(source)  # No le importa la gramatica
        parser: Parser = Parser(lexer)  # Si le importa la gramatica

        program: Program = parser.parse_program()

        self.assertEquals(len(program.statements), 2)

        for statement in program.statements:
            self.assertEquals(statement.token_literal(), 'retorna')
            self.assertIsInstance(statement, ReturnStatement)

    def test_identifier_expression(self) -> None:
        source: str = 'foobar;'
        lexer: Lexer = Lexer(source)  # No le importa la gramatica
        parser: Parser = Parser(lexer)  # Si le importa la gramatica

        program: Program = parser.parse_program()

        # Funcion Auxiliar que dice los errores
        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None

        self._test_literal_expression(
            expression_statement.expression, 'foobar')

    def _test_program_statements(self,
                                 parser: Parser,
                                 program: Program,
                                 expected_statement_count: int = 1) -> None:
        if parser.errors:
            print(parser.errors)

        self.assertEquals(len(parser.errors), 0)
        self.assertEquals(len(program.statements), expected_statement_count)
        self.assertIsInstance(program.statements[0], ExpressionStatement)

    def _test_literal_expression(self,
                                expression: Optional[Expression],
                                expected_value: Any) -> None:
        value_type: Type = type(expected_value)

        if value_type == str:
            self._test_identifier(expression, expected_value)
        elif value_type == int:
            self._test_integer(expression, expected_value)
        elif value_type == bool:
            self._test_boolean(expression, expected_value)
        else:
            self.fail(f'Tipo de expresión no controlada. Obtuvo={value_type}')

    def _test_identifier(self,
                         expression: Optional[Expression],
                         expected_value: str) -> None:
        self.assertIsInstance(expression, Identifier)

        identifier = cast(Identifier, expression)
        self.assertEquals(identifier.value, expected_value)
        self.assertEquals(identifier.token.literal, expected_value)
    '''

    5;
    variable x = 5;
    suma(5, 10);
    5 + 5 + 5;

    '''

    def test_integer_expressions(self) -> None:
        source: str = '5;'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        expression_statement = cast(ExpressionStatement, program.statements[0])

        assert expression_statement.expression is not None
        self._test_literal_expression(expression_statement.expression, 5)

    def _test_integer(self,
                      expression: Expression,
                      expected_value: int) -> None:
        self.assertIsInstance(expression, Integer)

        integer = cast(Integer, expression)
        self.assertEquals(integer.value, expected_value)
        self.assertEquals(integer.token.literal, str(expected_value))

    def _test_boolean(self,
                      expression: Expression,
                      expected_value: Boolean) -> None:
        self.assertIsInstance(expression, Boolean)

        boolean = cast(Boolean, expression)
        self.assertEquals(boolean.value, expected_value)
        self.assertEquals(boolean.token.literal, 'verdadero' if expected_value else 'falso')
        
    '''
    Operadores de prefijo:
    -5;
    !foo;
    5 + -10;

    Test
    Nodo
    Identificar funcion especifica para parsear el nodo y
    registrarla como infix o prefix
    '''

    def test_prefix_expressions(self) -> None:
        source: str = '!5; -15; !verdadero'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)
        # TODO
        program: Program = parser.parse_program()

        self._test_program_statements(parser,
                                      program,
                                      expected_statement_count=3)
        
        for statement, (expected_operator, expected_value) in zip(
            program.statements, [('!', 5), ('-', 15), ('!', True)]):
            statement = cast(ExpressionStatement, statement)
            self.assertIsInstance(statement.expression, Prefix)

            prefix = cast(Prefix, statement.expression)
            self.assertEquals(prefix.operator, expected_operator)

            assert prefix.right is not None
            self._test_literal_expression(prefix.right, expected_value)

    '''
    Ejemplos de infix:
    (el signo de en medio es infix)

    5 + 5;
    5 - 5;
    5 * 5;
    5 / 5;
    5 > 5;
    5 < 5;
    5 == 5;
    5 != 5;
    '''
    def test_infix_expressions(self) -> None:
        source: str='''
            5 + 5;
            5 - 5;
            5 * 5;
            5 / 5;
            5 > 5;
            5 < 5;
            5 == 5;
            5 != 5;
            verdadero == verdadero;
        '''
        
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statement_count=9)

        expected_operators_and_values: list[tuple[Any, str, Any]] = [
            (5, '+', 5),
            (5, '-', 5),
            (5, '*', 5),
            (5, '/', 5),
            (5, '>', 5),
            (5, '<', 5),
            (5, '==', 5),
            (5, '!=', 5),
            (True, '==', True),
        ]

        for statement, (expected_left, expected_operator, expected_right) in zip(
            program.statements, expected_operators_and_values):
            statement = cast(ExpressionStatement, statement)
            assert statement.expression is not None
            self.assertIsInstance(statement.expression, Infix)
            self._test_infix_expression(
                statement.expression,
                expected_left,
                expected_operator,
                expected_right)

    def _test_infix_expression(
            self,
            expression: Expression,
            expected_left: Any,
            expected_operator: str,
            expected_right: Any):
        infix = cast(Infix, expression)

        assert infix.left is not None
        self._test_literal_expression(infix.left, expected_left)

        assert infix.right is not None
        self._test_literal_expression(infix.right, expected_right)

    '''
    Booleanos

    verdadero;
    falso;
    variable foo = verdadero;
    variable bar = falso;
    '''
    
    def test_boolean_expression(self) -> None:
        source: str='verdadero; falso;'
        
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program, expected_statement_count=2) # True False
        
        expected_values: list[bool] = [True, False]

        for statement, expected_value in zip(program.statements, expected_values):
            expression_statement = cast(ExpressionStatement, statement)

            assert expression_statement is not None
            self._test_literal_expression(expression_statement.expression, expected_value)
    
    '''
        1str: programa inicial, 
        2str: Orden de precedencia dentro del programa
        int: Cuantos statements se espera del programa
    '''

    def test_operator_precedence(self) -> None:
        test_sources: list[tuple[str, str, int]] = [
            ('-a * b;', '((-a) * b)', 1),
            ('!-a;', '(!(-a))', 1),
            ('a + b + c;', '((a + b) + c)', 1),
            ('a + b - c;', '((a + b) - c)', 1),
            ('a * b * c;', '((a * b) * c)', 1),
            ('a + b / c;', '(a + (b / c))', 1),
            ('a * b / c;', '((a * b) / c)', 1),
            ('a + b * c + d / e - f;', '(((a + (b * c)) + (d / e)) - f)', 1),
            ('5 > 4 == 3 < 4;', '((5 > 4) == (3 < 4))', 1),
            ('3 - 4 * 5 == 3 * 1 + 4 * 5;', '((3 - (4 * 5)) == ((3 * 1) + (4 * 5)))', 1),
            ('3 + 4; -5 * 5;', '(3 + 4)((-5) * 5)', 2),
            ('verdadero;', 'verdadero', 1),
            ('falso;', 'falso', 1),
            ('3 > 5 == verdadero;', '((3 > 5) == verdadero)', 1),
            ('3 < 5 == falso;', '((3 < 5) == falso)', 1),
            ('1 + (2 + 3) + 4;', '((1 + (2 + 3)) + 4)', 1),
            ('(5 + 5) * 2;', '((5 + 5) * 2)', 1),
            ('2 / (5 + 5);', '(2 / (5 + 5))', 1),
            ('-(5 + 5);', '(-(5 + 5))', 1),
            # LLAMADAS A FUNCIONES
            ('a + suma(b * c) + d;', '((a + suma(b * c))) + d)', 1),
            ('suma(a, b, 1, 2 * 3, 4 + 5, suma(6, 7 * 8));',
             'suma(a, b, 1, (2 * 3), (4 + 5), suma(6, (7 * 8)))', 1),
            ('suma(a + b + c * d / f + g);', 'suma((((a + b) + ((c * d) / f)) + g))', 1),
        ]

        for source, expected_result, expected_statement_count in test_sources:
            lexer: Lexer = Lexer(source)
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            self._test_program_statements(parser, program, expected_statement_count)
            self.assertEquals(str(program), expected_result)

    ''' 

        CICLO IF
        --------------------

        si (x > y) {
            retorna x;
        } si_no {
            retorna y;
        }

        --------------------

        si (x > y) {
            regresa x;
        }

        --------------------

        variable foo = si (x > y) { x } si_no { y }

        --------------------

        si (<condicion>) <consecuencia> si_no <alternativa>

        --------------------
    '''

    def test_if_expression(self) -> None:
        source: str = ' si (x < y) { z }'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Esto es para comprobar que el primer statement sea un ExpressionStatement y con eso
        # sabemos que tenemos un expression que debe ser un if
        if_expression = cast(If, cast(ExpressionStatement, program.statements[0]).expression)
        self.assertIsInstance(if_expression, If)

        # Comprobamos la condicion
        assert if_expression.condition is not None
        self._test_infix_expression(if_expression.condition, 'x', '<', 'y')

        # Comprobamos la consecuencia
        assert if_expression.consequence is not None
        self.assertIsInstance(if_expression.consequence, Block)
        self.assertEquals(len(if_expression.consequence.statements), 1)

        consequence_statement = cast(ExpressionStatement, 
                                     if_expression.consequence.statements[0])
        
        assert consequence_statement.expression is not None
        self._test_identifier(consequence_statement.expression, 'z')

        # Comprobamos la alternativa
        # Nos aseguramos que sea None, que no existe alternativa (Sino)
        self.assertIsNone(if_expression.alternative)

    def test_if_else_expression(self) -> None:
        source: str = 'si (x != y) { x } si_no { y }'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Test correct node type
        if_expression = cast(If, cast(ExpressionStatement, program.statements[0]).expression)
        self.assertIsInstance(if_expression, If)

        # Test condition
        assert if_expression.condition is not None
        self._test_infix_expression(if_expression.condition, 'x', '!=', 'y')

        # Test consequence
        assert if_expression.consequence is not None
        self.assertIsInstance(if_expression.consequence, Block)
        self.assertEquals(len(if_expression.consequence.statements), 1)

        consequence_statement = cast(ExpressionStatement, if_expression.consequence.statements[0])
        assert consequence_statement.expression is not None
        self._test_identifier(consequence_statement.expression, 'x')

        # Test alternative
        assert if_expression.alternative is not None
        self.assertIsInstance(if_expression.alternative, Block)
        self.assertEquals(len(if_expression.alternative.statements), 1)

        alternative_statement = cast(ExpressionStatement, if_expression.alternative.statements[0])
        assert alternative_statement.expression is not None
        self._test_identifier(alternative_statement.expression, 'y')


        '''
        ###### FUNCIONES ######

        procedimiento (x, y) {
            regresa x + y;
        }

        procedimiento () { regresa verdadero }

        mi_func(x, y, procedimiento(x, y) { regresa x != y} )

        procedimiento <paramteros> <bloque>

        <parametros> = (<param_1>, <param_2>, <param_3>, ...)
        '''

    def test_function_literal(self) -> None:
        source: str = 'funcion(x, y) {x + y}'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Probramos que tengamo el nodo correcto (FUNCION)

        function_literal = cast(Function, cast(ExpressionStatement,
                                               program.statements[0]).expression)
        
        self.assertIsInstance(function_literal, Function)

        # Probamos que los parametros sean 2
        self.assertEquals(len(function_literal.parameters), 2)
        self._test_literal_expression(function_literal.parameters[0], 'x')
        self._test_literal_expression(function_literal.parameters[1], 'y')

        # Probamos el bloque (cuerpo) (no siempre lo tiene)
        assert function_literal.body is not None
        self.assertEquals(len(function_literal.body.statements), 1) # -> Un statement 'x + y'

        body = cast(ExpressionStatement, function_literal.body.statements[0])
        assert body.expression is not None
        self._test_infix_expression(body.expression, 'x', '+', 'y')

    def test_function_parameters(self) -> None:
        tests = [
            {'input': 'funcion() {};',
             'expected_params': []},
            {'input': 'funcion(x) {};',
             'expected_params': ['x']},
            {'input': 'funcion(x, y, z) {};',
             'expected_params': ['x', 'y', 'z']}
        ]

        for test in tests:
            lexer: Lexer = Lexer(test['input']) # type: ignore
            parser: Parser = Parser(lexer)

            program: Program = parser.parse_program()

            function = cast(Function, cast(ExpressionStatement,
                                           program.statements[0]).expression)

            self.assertEquals(len(function.parameters), len(test['expected_params']))

            for idx, param in enumerate(test['expected_params']):
                self._test_literal_expression(function.parameters[idx], param)

    '''
    Llamada de funciones:

    suma(2, 3);
    suma(2 + 2, 5 * 4 * 3)

    funcion(x, y) { x + y }(2, 3);
    mapea([1, 2, 3], funcion(x) { 2 * x} )

    <expresion>(<expresion_1>, <expresion_2>, ...)

    la llamada puede ser un infix por el parentesis

    '''

    def test_call_expression(self) -> None:
        source: str = 'suma(1, 2 * 3, 4 + 5);'
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()

        self._test_program_statements(parser, program)

        # Call es un nodo, el nodo de llamada

        call = cast(Call, cast(ExpressionStatement,
                               program.statements[0]).expression)
        
        
        self.assertIsInstance(call, Call)
        self._test_identifier(call.function, 'suma')

        # Testeamos los argumentos
        assert call.arguments is not None
        self.assertEquals(len(call.arguments), 3)
        # Vamos comprobando cada argumento
        self._test_literal_expression(call.arguments[0], 1)
        self._test_literal_expression(call.arguments[1], 2, '*', 3)
        self._test_literal_expression(call.arguments[2], 4, '+', 5)
        

    