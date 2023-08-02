from unittest import TestCase
from lpp.ast import (
    Identifier,
    LetStatement,
    Program,
    ReturnStatement
)
from lpp.token import (
    Token,
    TokenType,
)


class ASTTest(TestCase):
    def test_let_statement(self) -> None:
        # 'variable mi_var = otra_var;' <- Es un LetStatement porque es una declaracion de varibale
        #             ID        ID
        program: Program = Program(statements=[
            LetStatement(
                token=Token(TokenType.LET, literal='variable'),
                name=Identifier( 
                    token=Token(TokenType.IDENT, literal='mi_var'),
                    value='mi_var'
                ),
                value=Identifier(
                    token=Token(TokenType.IDENT, literal='otra_var'),
                    value='otra_var'
                )
            ),
        ])

        program_str = str(program)

        self.assertEquals(program_str, 'variable mi_var = otra_var;')

    def test_return_statement(self) -> None:
        # 'retorna mi_var;' <- Es un LetStatement porque es una declaracion de varibale
        #             ID        ID
        program: Program = Program(statements=[
            ReturnStatement(
                token=Token(TokenType.RETURN, literal="retorna"),
                return_value=Identifier(
                    token=Token(TokenType.IDENT, literal="mi_var"),
                    value="mi_var"
                )
            ),
        ])

        program_str = str(program)

        self.assertEquals(program_str, 'retorna mi_var;')
