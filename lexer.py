#Contains the lexer that converts input code into tokens.
# lexer.py

import re

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

# Token types for lexer implementation
INT = 'INT'
BOOL = 'BOOL'
STRING = 'STRING'
IF = 'IF'
ELSE = 'ELSE'
FOR = 'FOR'
PRINT = 'PRINT'
INPUT = 'INPUT'
FUNC = 'FUNC'
TRUE = 'TRUE'
FALSE = 'FALSE'

# Data type specifiers
INT_TYPE = 'INT_TYPE'
BOOL_TYPE = 'BOOL_TYPE'
STRING_TYPE = 'STRING_TYPE'

# Operators
PLUS = 'PLUS'
MINUS = 'MINUS'
MUL = 'MUL'
DIV = 'DIV'
MOD = 'MOD'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'
EQ = 'EQ'
NEQ = 'NEQ'
LT = 'LT'
GT = 'GT'
LE = 'LE'
GE = 'GE'
ASSIGN = 'ASSIGN'
ARROW = 'ARROW'
INPUT = 'INPUT'

# Punctuation
SEMI = 'SEMI'
COMMA = 'COMMA'
LPAREN = 'LPAREN'
RPAREN = 'RPAREN'
LBRACE = 'LBRACE'
RBRACE = 'RBRACE'
LBRACKET = 'LBRACKET'
RBRACKET = 'RBRACKET'

# Literals
INTEGER = 'INTEGER'
STRING_LITERAL = 'STRING_LITERAL'
BOOLEAN = 'BOOLEAN'

# Identifier
IDENTIFIER = 'IDENTIFIER'

# End of file marker
EOF = 'EOF'

# Lexer class definition
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos] if self.text else None

    def advance(self):
        """Advance the 'pos' and set 'current_char'."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def peek(self, ahead=1):
        """Peek ahead 'ahead' characters without consuming them."""
        peek_pos = self.pos + ahead
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multi-digit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    """Special character handling here please and \ and more"""
    def string(self):
        """Return a string consumed from the input."""
        result = ''
        self.advance()  # Skip the opening quote
        while self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip the closing quote
        return result

    def _id(self):
        """Handle identifiers and reserved keywords."""
        result = ''
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            result += self.current_char
            self.advance()
        token = self.check_keyword(result)
        return token if token else Token(IDENTIFIER, result)

    def check_keyword(self, word):
        """Check for reserved keywords."""
        keywords = {
            "int": INT_TYPE,
            "bool": BOOL_TYPE,
            "string": STRING_TYPE,
            "if": IF,
            "else": ELSE,
            "for": FOR,
            "print": PRINT,
            "input": INPUT,
            "func": FUNC,
            "true": TRUE,
            "false": FALSE
        }
        return Token(keywords[word], word) if word in keywords else None

    def get_next_token(self):
        """Tokenize the input."""
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            
            if self.text[self.pos:self.pos+6] == 'input(' and self.peek(5) == ')':
                self.pos += 6  # Advance past 'input('
                self.advance()  # Advance past ')'
                return Token(INPUT, 'input()')

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char == '"':
                return Token(STRING_LITERAL, self.string())

            if self.current_char.isalpha() or self.current_char == '_':
                id_token = self._id()
                if id_token.type in [TRUE, FALSE]:
                    return Token(BOOLEAN, id_token.value == "true")
                return id_token

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
            
            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')
            
            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')
            
            if self.current_char == '%':
                self.advance()
                return Token(MOD, '%')

            if self.current_char == '=':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(EQ, '==')
                elif self.peek() == '>':
                    self.advance()
                    self.advance()
                    return Token(ARROW, '=>')
                else:
                    self.advance()
                    return Token(ASSIGN, '=')
            
            if self.current_char == '<' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(LE, '<=')
            elif self.current_char == '<':
                self.advance()
                return Token(LT, '<')
            
            if self.current_char == '>' and self.peek() == '=':
                self.advance()
                self.advance()
                return Token(GE, '>=')
            elif self.current_char == '>':
                self.advance()
                return Token(GT, '>')
            
            if self.current_char == '!':
                if self.peek() == '=':
                    self.advance()
                    self.advance()
                    return Token(NEQ, '!=')
                else:
                    self.advance()
                    return Token(NOT, '!')
            
            if self.current_char == '&':
                if self.peek() == '&':
                    self.advance()
                    self.advance()
                    return Token(AND, '&&')
            
            if self.current_char == '|':
                if self.peek() == '|':
                    self.advance()
                    self.advance()
                    return Token(OR, '||')
            
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')
            
            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')
            
            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')
            
            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
            if self.current_char == '{':
                self.advance()
                return Token(LBRACE, '{')
            
            if self.current_char == '}':
                self.advance()
                return Token(RBRACE, '}')
            
            if self.current_char == '[':
                self.advance()
                return Token(LBRACKET, '[')

            if self.current_char == ']':
                self.advance()
                return Token(RBRACKET, ']')
        
            self.error()

        return Token(EOF, None)

    def error(self):
        raise Exception('Invalid character')
    
# Helper function to test lexer
def run_lexer(text):
    lexer = Lexer(text)
    token = lexer.get_next_token()
    while token.type != EOF:
        print(token)
        token = lexer.get_next_token()

# Example usage
if __name__ == "__main__":
    input_text = 'int x = input()'
    run_lexer(input_text)
