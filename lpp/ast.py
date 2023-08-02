from abc import (
    ABC, 
    abstractmethod,
)
from typing import Optional
from lpp.token import Token

# Aqui se generan 3 nods independientes

# abc -> abstract syntax class

# 1 Nodo abstracto que extiende la clase ABC para representar clases abstractas
# Estos son los nodos principales que extienden todos los demas nodos (ASTNodo, Statement, Expression)

class ASTNode(ABC):
    
    @abstractmethod
    def token_literal(self) -> str:
        pass
    
    @abstractmethod
    def __str__(self) -> str:
        pass

# 2 Es un nodo de un AST
# Nunca vamos a inicializar Statement de forma directa, la vamos a inicializar de forma extensiva
class Statement(ASTNode): 
    def __init__(self, token: Token) -> None:
        self.token = token
    
    def token_literal(self) -> str:
        # Retorna la literal que existe en el token, el pedazo de string de nuestro programa
        return self.token.literal 

# 3 Es un nodo de un AST
class Expression(ASTNode):
    def __init__(self, token: Token) -> None:
        self.token = token

    def token_literal(self) -> str:
        return self.token.literal

# Esta es la definicion del programa    
class Program(ASTNode):

    def __init__(self, statements: list[Statement]) -> None:
        self.statements = statements

    def token_literal(self) -> str:
        # Verificamos si hay mas de 1 statement
        if len(self.statements) > 0:
            # Regresamos el token literal del PRIMER statement
            # Solo es para el debug, para los tests
            return self.statements[0].token_literal()
        return ''
    
    # Concatenamos todos los statements
    def __str__(self) -> str:
        out: list[str] = []
        for statement in self.statements:
            out.append(str(statement))

        # ''.join(out) -> Toda la concatenacion hecha
        return ''.join(out)

# Nodo de identificador y letstatement
# LEctura de arriba hacia abajo (de Python)

class Identifier(Expression):
    def __init__(self, token: Token, value: str) -> None:
        super().__init__(token)
        self.value = value

    def __str__(self) -> str:
        return self.value

class LetStatement(Statement):
    def __init__(self, token: Token, name: Optional[Identifier] = None, value: Optional[Expression] = None) -> None:
        # Estamos extendiendo Statement
        super().__init__(token)
        self.name = name
        self.value = value

    def __str__(self) -> str:
        return f'{self.token_literal()} {str(self.name)} = {str(self.value)};'
    
class ReturnStatement(Statement):
    
    def __init__(self,
                 token: Token,
                 return_value: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.return_value = return_value

    def __str__(self) -> str:
        return f'{self.token_literal()} {str(self.return_value)};'
    
class ExpressionStatement(Statement):
    def __init__(self, 
                 token: Token,
                 expression: Optional[Expression] = None) -> None:
        super().__init__(token)
        self.expression = expression

    def __str__(self) -> str:
        return str(self.expression)
