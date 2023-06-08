from lpp.lexer import Lexer
from lpp.token import (
    Token,
    TokenType,
)
# Esto nos dice que ya terminamos, que ya se acaba la oracion
EOF_TOKEN: Token = Token(TokenType.EOF, '')

def start_repl() -> None:
    # Se usa el operador morsa aqui xd
    while (source := input('>> ')) != 'salir()':
        lexer: Lexer = Lexer(source)

        # Mientras el proximo token no sea igual al 'salir()'
        # imprime el token
        while(token := lexer.next_token()) != EOF_TOKEN:
            print(token)
