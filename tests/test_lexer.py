from unittest import TestCase
from lpp.token import Token,TokenType 

from lpp.lexer import Lexer

class LexerTest(TestCase):

    def test_illegal(self) -> None:
        source: str = '¡¿@' #Caracteres ilegales dentro nuestro lenguaje
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.ILLEGAL, '¡'),
            Token(TokenType.ILLEGAL, '¿'),
            Token(TokenType.ILLEGAL, '@'),
        ]

        self.assertEqual(tokens, expected_tokens) #Compara de que los tokens sean iguales a los expected tokens

    def test_one_character_operator(self) -> None:
        source: str = '=+-/*<>!'
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.MINUS, '-'),
            Token(TokenType.DIVIDE, '/'),
            Token(TokenType.MULT, '*'),
            Token(TokenType.LT, '<'),
            Token(TokenType.MT, '>'),
            Token(TokenType.NOT, '!'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_eof(self) -> None: #Es para indicar que ya se acabo el programa/codigo
        source: str = '+'
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(len(source)+1):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.PLUS, '+'),
            Token(TokenType.EOF, ''),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_delimiters(self) -> None:
        source = '(){},;'
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(len(source)):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.LPAREN, '('),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_assignment(self) -> None:  # Asignacion de variable
        source: str = 'variable cinco = 5;'
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(5):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'cinco'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.INT, '5'),
            Token(TokenType.SEMICOLON, ';'),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_function_declaration(self) -> None:
        source: str = '''
            variable suma = funcion(x,y) {
                x + y;
            };
        '''
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(16):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'suma'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.FUNCTION, 'funcion'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.IDENT, 'x'),
            Token(TokenType.PLUS, '+'),
            Token(TokenType.IDENT, 'y'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)


    def test_function_call(self) -> None:
        source: str = 'variable resultado = suma(dos, tres);'

        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(10):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.LET, 'variable'),
            Token(TokenType.IDENT, 'resultado'),
            Token(TokenType.ASSIGN, '='),
            Token(TokenType.IDENT, 'suma'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.IDENT, 'dos'),
            Token(TokenType.COMMA, ','),
            Token(TokenType.IDENT, 'tres'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEqual(tokens, expected_tokens)

    def test_control_statement(self) -> None:
        source: str = '''
            si (5 < 10) {
                retorna verdadero;
            } si_no {
                retorna falso;
            }
        '''
        lexer: Lexer = Lexer(source)
        tokens: list[Token] = []
        for i in range(17):
            tokens.append(lexer.next_token())
        
        expected_tokens: list[Token] = [
            Token(TokenType.IF, 'si'),
            Token(TokenType.LPAREN, '('),
            Token(TokenType.INT, '5'),
            Token(TokenType.LT, '<'), #MENOR - NUEVO
            Token(TokenType.INT, '10'),
            Token(TokenType.RPAREN, ')'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'retorna'),
            Token(TokenType.TRUE, 'verdadero'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
            Token(TokenType.ELSE, 'si_no'),
            Token(TokenType.LBRACE, '{'),
            Token(TokenType.RETURN, 'retorna'),
            Token(TokenType.FALSE, 'falso'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.RBRACE, '}'),
        ]
        self.assertEqual(tokens, expected_tokens)

    def test_two_character_operator(self) -> None:
        source: str = '''
            10 == 10;
            10 != 9;
        '''
        lexer: Lexer = Lexer(source)

        tokens: list[Token] = []
        for i in range(8):
            tokens.append(lexer.next_token())

        expected_tokens: list[Token] = [
            Token(TokenType.INT, '10'),
            Token(TokenType.EQUALS, '=='),
            Token(TokenType.INT, '10'),
            Token(TokenType.SEMICOLON, ';'),
            Token(TokenType.INT, '10'),
            Token(TokenType.NOTEQUALS, '!='),
            Token(TokenType.INT, '9'),
            Token(TokenType.SEMICOLON, ';'),
        ]

        self.assertEquals(tokens, expected_tokens)