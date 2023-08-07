from lpp.ast import Program
from lpp.lexer import Lexer
from lpp.parser import Parser
from lpp.token import (
    Token,
    TokenType,
)

# Esto nos dice que ya terminamos, que ya se acaba la oracion
EOF_TOKEN: Token = Token(TokenType.EOF, '')

def _print_parse_errors(errors: list[str]):
    for error in errors:
        print(error)

def start_repl() -> None:
    # Se usa el operador morsa aqui
    while (source := input('>> ')) != 'salir()':
        lexer: Lexer = Lexer(source)
        parser: Parser = Parser(lexer)

        program: Program = parser.parse_program()
        # Mientras el proximo token no sea igual al 'salir()'
        # imprime el token
        # while(token := lexer.next_token()) != EOF_TOKEN:
        #     print(token)

        if len(parser.errors) > 0:
            _print_parse_errors(parser.errors)
            continue

        print(program)
