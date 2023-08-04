from lpp.ast import (
    Program, 
    Statement, 
    LetStatement, 
    Identifier, 
    ReturnStatement,
    Expression,
    ExpressionStatement,
    Integer,
    Prefix,
    Infix,
    Boolean,
    )
from lpp.lexer import Lexer
from lpp.token import TokenType, Token
from typing import Optional, Callable
from enum import IntEnum

'''
    Parser es el Analizador Lexico en Python
'''



# Prefix Parse Funcion no recibe parametros y opcionalmente regresa una expresion, para eso es el Optional, si falla solo regrese un None
PrefixParseFn = Callable[[], Optional[Expression]]
# Infix Parse Funcion recibe una lista de expresiones como parametro y opcionalmente regresa una expresion
InfixParseFn = Callable[[Expression], Optional[Expression]]
# Prefix Parse FuncionES, diccionario que va a identificar con el tipo de token y va regreser el prefixfn
PrefixParseFns = dict[TokenType, PrefixParseFn]
# Infix Parse FuncionES, lo mismo que el de arriba pero regresa un InfixFn
InfixParseFns = dict[TokenType, InfixParseFn]

'''
    Prefix (Prefijo)
    Infix (Infijo) se refiere a que por ejemplo: 
            2 + 2
        El operador se encuentra entre dos elementos   
'''



# El precedence de mas alto valor se evalua primero
class Precedence(IntEnum):
    LOWEST = 1              # Presencia mas baja
    EQUALS = 2              # Presencia mas alta
    LESSGREATER = 3         # Mas o menos
    SUM = 4                 # Si tenemos una suma y luego un less greater primero se hace la suma
    PRODUCT = 5             # Primero el producto
    PREFIX = 6              # Prefijo
    CALL = 7                # Llamada a funcion

PRECEDENCES: dict[TokenType, Precedence] = {
    TokenType.EQUALS: Precedence.EQUALS,
    TokenType.NOTEQUALS: Precedence.EQUALS,
    TokenType.LT: Precedence.LESSGREATER,
    TokenType.MT: Precedence.LESSGREATER,
    TokenType.PLUS: Precedence.SUM,
    TokenType.MINUS: Precedence.SUM,
    TokenType.DIVIDE: Precedence.PRODUCT,
    TokenType.MULT: Precedence.PRODUCT,
}


class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None
        self._errors: list[str] = []

        # Registra toda las funciones
        self._prefix_parse_fns: PrefixParseFns = self._register_prefix_parse_fns()
        self._infix_parse_fns: InfixParseFns = self._register_infix_parse_fns()

        self._advance_tokens()
        self._advance_tokens()
    
    @property # -> Propiedad privada, es solo Leer (Read Only)
    def errors(self) -> list[str]:
        return self._errors

    def parse_program(self) -> Program:
        program: Program = Program(statements=[])

        assert self._current_token is not None

        while self._current_token.token_type != TokenType.EOF:
            statement = self._parse_statement()
            if statement is not None:
                # Se agrega statemente por statement al program
                program.statements.append(statement)

            self._advance_tokens()

        return program
    
    # Es como el next_caracter, solo que este pasa al siguiente Token
    def _advance_tokens(self) -> None:
        self._current_token = self._peek_token
        # Avanzamos a otro token
        self._peek_token = self._lexer.next_token()

    # Buscamos que precedencia tiene le token
    def _current_precedence(self) -> Precedence:
        assert self._current_token is not None
        try:
            return PRECEDENCES[self._current_token.token_type]
        except KeyError:
            return Precedence.LOWEST
    
    # Comienza a identificar si la sintaxis es correcta
    def _expected_token(self, token_type: TokenType) -> bool:
        assert self._peek_token is not None

        if self._peek_token.token_type == token_type:
            self._advance_tokens()
            
            return True  
        # Aqui se le pasa el error
        self._expected_token_error(token_type)
        return False
    
    def _expected_token_error(self, token_type: TokenType) -> None:
        assert self._peek_token is not None
        error = f'Se esperaba que el siguiente token fuera {token_type} ' + \
                f'pero se obtuvo {self._peek_token.token_type}'
        
        self._errors.append(error)

    def _parse_expression(self, precedence: Precedence) -> Optional[Expression]:
        assert self._current_token is not None
        try:
            prefix_parse_fn = self._prefix_parse_fns[self._current_token.token_type]
        except KeyError:
            message = f'No se encontro ninguna funcion para parsear {self._current_token.literal}'
            self._errors.append(message)
            return None
        
        # Expresion de izquierda
        left_expression = prefix_parse_fn()

        assert self._peek_token is not None
        while not self._peek_token.token_type == TokenType.SEMICOLON and precedence < self._peek_precedence():
            try:
                infix_parse_fn = self._infix_parse_fns[self._peek_token.token_type]

                self._advance_tokens()

                assert left_expression is not None
                left_expression = infix_parse_fn(left_expression)
            except KeyError:
                return left_expression

        return left_expression

    def _parse_expression_statement(self) -> Optional[ExpressionStatement]:
        assert self._current_token is not None
        expression_statement = ExpressionStatement(token=self._current_token)

        expression_statement.expression = self._parse_expression(Precedence.LOWEST)

        assert self._peek_token is not None
        if self._peek_token.token_type == TokenType.SEMICOLON:
            self._advance_tokens()

        return expression_statement
        

    def _parse_let_statement(self) -> Optional[LetStatement]:
        assert self._current_token is not None

        let_statement = LetStatement(token=self._current_token)

        # Si el token no es identificador ya fallo
        if not self._expected_token(TokenType.IDENT):
            return None
        
        let_statement.name = self._parse_identifier()

        # Si el siguiente token no es asignacion '=' fallo
        if not self._expected_token(TokenType.ASSIGN):
            return None
        
        # TODO terminar cuando sepa parsear expresiones

        # Avanzamos hasta que llegue a ';' (Hasta que termine)
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()

        return let_statement

    def _parse_statement(self) -> Optional[Statement]:
        assert self._current_token is not None

        if self._current_token.token_type == TokenType.LET:
            return self._parse_let_statement()
        elif self._current_token.token_type == TokenType.RETURN:
            return self._parse_return_statement()
        else:
            return self._parse_expression_statement()

    def _parse_return_statement(self) -> Optional[ReturnStatement]:
        assert self._current_token is not None

        return_statement = ReturnStatement(token = self._current_token)
        self._advance_tokens()

        # TODO Terminar cuando sepamos parsear expresiones
        while self._current_token.token_type != TokenType.SEMICOLON:
            self._advance_tokens()

        return return_statement
    
    def _parse_identifier(self) -> Identifier:
        assert self._current_token is not None

        return Identifier(token=self._current_token,
                          value=self._current_token.literal)
    
    def _parse_integer(self) -> Optional[Integer]:
        assert self._current_token is not None

        integer = Integer(token=self._current_token)
        try:
            integer.value = int(self._current_token.literal)
        except ValueError:
            message = f'No se ha podido parsear {self._current_token.literal}  ' + \
                        'como entero.'
            self._errors.append(message)

            return None
        
        return integer
    

    # def _parse_integer(self) -> Float:
    #        pass
    # Identifica esto:  -5;
    #                   !foo;
    #                   5 + -10;
    def _parse_prefix_expression(self) -> Prefix:
        assert self._current_token is not None
        prefix_expression = Prefix(token=self._current_token,
                                   operator=self._current_token.literal)
        self._advance_tokens()
        prefix_expression.right = self._parse_expression(Precedence.PREFIX)

        return prefix_expression
    
    def _parse_infix_expression(self, left: Expression) -> Infix:
        assert self._current_token is not None
        infix = Infix(token=self._current_token,
                      operator=self._current_token.literal,
                      left=left)
        

        # Con esto se agrupa la expresion, con la precedencia
        precedence = self._current_precedence()

        self._advance_tokens()


        # Recursivamente evalua la expresion y si hay un infix regresa
        # de manera recursiva
        infix.right = self._parse_expression(precedence)

        return infix
    
    def _peek_precedence(self) -> Precedence:
        assert self._peek_token is not None
        try:
            return PRECEDENCES[self._peek_token.token_type]
        except KeyError:
            return Precedence.LOWEST
        
    def _parse_boolean(self) -> Boolean:
        assert self._current_token is not None

        return Boolean(token=self._current_token,
                       value=self._current_token.token_type == TokenType.TRUE)

    



    def _register_infix_parse_fns(self) -> InfixParseFns:
        return {
            TokenType.PLUS: self._parse_infix_expression,
            TokenType.MINUS: self._parse_infix_expression,
            TokenType.DIVIDE: self._parse_infix_expression,
            TokenType.MULT: self._parse_infix_expression,
            TokenType.EQUALS: self._parse_infix_expression,
            TokenType.NOTEQUALS: self._parse_infix_expression,
            TokenType.LT: self._parse_infix_expression,
            TokenType.MT: self._parse_infix_expression,
        }
    
    def _register_prefix_parse_fns(self) -> PrefixParseFns:
        return {
            TokenType.IDENT: self._parse_identifier,
            TokenType.INT: self._parse_integer,
            TokenType.MINUS: self._parse_prefix_expression,
            TokenType.NOT: self._parse_prefix_expression,
            TokenType.TRUE: self._parse_boolean,
            TokenType.FALSE: self._parse_boolean,
        }

    