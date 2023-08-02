from enum import (
    auto,
    Enum,
    unique,
)
from typing import NamedTuple

@unique
class TokenType(Enum):
    ASSIGN = auto() # =
    COMMA = auto() # ,
    EOF = auto() #Termino el archivo
    FUNCTION = auto() #Uno funcion
    IDENT = auto() #Identificador o nombre de nuestras variables
    ILLEGAL = auto() #Cuando un token no peretenece a nuestro lenguaje
    INT = auto() #Numero entero
    RBRACE = auto() #Llave izquierda
    LET = auto() #Definicion dde variables
    LPAREN = auto()
    LBRACE = auto() # llave derecha
    PLUS = auto() #Simbolo de suma
    RPAREN = auto() #Parentesis derecho
    SEMICOLON = auto() # punto y coma ;
    ELSE = auto() # si_no
    IF = auto() # if
    RETURN = auto() # Retorna
    LT = auto() # Menor que
    MT = auto() # Mayor que
    TRUE = auto() # verdadero
    FALSE = auto() # falso
    MINUS = auto() # Signo Menos
    DIVIDE = auto() # Signo Dividir
    MULT = auto() # Signo Multiplicacion
    NOT = auto() # not
    EQUALS = auto() # es ==
    NOTEQUALS = auto() # es !=
    FLOAT = auto() # es float
    FOR = auto()

class Token(NamedTuple):
    token_type: TokenType
    literal: str

    def __str__(self) -> str: #Funcion que regresa un str
        return f'Type: {self.token_type}, literal: {self.literal}'
    
# Funcion auxiliar dentro del token que nos permite saber si 
# estamos dentro de un keyboard o un identificador ( nombre de la variable)
def lookup_token_type(literal: str) -> TokenType:
    #Diccionario, con llaves str y valores TT
    keywords: dict[str, TokenType] = {
        'falso': TokenType.FALSE,
        'verdadero': TokenType.TRUE,
        'retorna': TokenType.RETURN,
        'si': TokenType.IF,
        'si_no': TokenType.ELSE,
        'variable': TokenType.LET,
        'funcion': TokenType.FUNCTION,
        'para': TokenType.FOR,
    }

    return keywords.get(literal, TokenType.IDENT)
