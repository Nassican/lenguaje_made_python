from lpp.ast import Program, Statement, LetStatement, Identifier
from lpp.lexer import Lexer
from lpp.token import TokenType, Token
from typing import Optional

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self._lexer = lexer
        self._current_token: Optional[Token] = None
        self._peek_token: Optional[Token] = None

        self._advance_tokens()
        self._advance_tokens()

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
    
    # Comienza a identificar si la sintaxis es correcta
    def _expected_token(self, token_type: TokenType) -> bool:
        assert self._peek_token is not None

        if self._peek_token.token_type == token_type:
            self._advance_tokens()
            
            return True  
        
        return False

    def _parse_let_statement(self) -> Optional[LetStatement]:
        assert self._current_token is not None

        let_statement = LetStatement(token=self._current_token)

        # Si el token no es identificador ya fallo
        if not self._expected_token(TokenType.IDENT):
            return None
        
        let_statement.name = Identifier(token=self._current_token, value=self._current_token.literal)

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
        else:
            return None

    