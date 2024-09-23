"""Turn a input string into a stream of tokens with lexical analysis.

The `lexer(input_string: str)` function is the entry point. It generates a
stream of tokens from the `input_string`.

Examples:

    >>> from project1.lexer import lexer
    >>> input_string = ":\\n  \\n:"
    >>> for i in lexer(input_string):
    ...     print(i)
    ...
    (COLON,":",1)
    (COLON,":",3)
    (EOF,"",3)
"""

from typing import Iterator, List

from project1.token import Token, TokenType
from project1.fsm import FiniteStateMachine, Colon, Eof, WhiteSpace, run_fsm

def _is_last_token(token: Token) -> bool:
    return token.token_type == "EOF"

def _get_new_lines(value: str) -> int:
    return value.count("\n")

def _get_token(input_string: str, fsms: List[FiniteStateMachine]) -> Token:
    longest_match: Token = Token.undefined("") 
    longest_length: int = 0
    
    for fsm in fsms:
    
        num_chars_read, token = run_fsm(fsm, input_string)
        
        if num_chars_read > longest_length:
            longest_length = num_chars_read
            longest_match = token
            
    if longest_length == 0:
        return Token.eof("")

    return longest_match
    
def lexer(input_string: str) -> Iterator[Token]:
    
    fsms: list[FiniteStateMachine] = [Colon(), Eof(), WhiteSpace()]
    hidden: list[TokenType] = ["WHITESPACE"]
    line_num: int = 1
    token: Token = Token.undefined("")
    while not _is_last_token(token):
        token = _get_token(input_string, fsms)
        token.line_num = line_num
        line_num = line_num + _get_new_lines(token.value)
        input_string = input_string.removeprefix(token.value)
        if token.token_type in hidden:
            continue
        yield token
