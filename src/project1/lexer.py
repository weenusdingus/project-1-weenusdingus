from typing import Iterator, List

from project1.token import Token, TokenType
from project1.fsm import FiniteStateMachine, Colon, Eof, WhiteSpace, run_fsm, Comma, Period, Q_mark, Left_Paren, Right_Paren, ColonDash, Comment, Schemes, String, Rules, Queries, Facts, ID

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
            
    # If no FSM matches the input, return an undefined token with the first character
     if longest_length == 0:
        return Token.undefined(input_string[0])

     return longest_match

def lexer(input_string: str) -> Iterator[Token]:
    fsms: list[FiniteStateMachine] = [Colon(), Eof(), WhiteSpace(), Comma(), Period(), Q_mark(),Left_Paren(), Right_Paren(), ColonDash(), Comment(), Schemes(), String(), Rules(), Queries(), Facts(), ID()]
    hidden: list[TokenType] = ["WHITESPACE"]
    line_num: int = 1
    token: Token = Token.undefined("")
    while not _is_last_token(token):
        token = _get_token(input_string, fsms)
        token.line_num = line_num
        line_num = line_num + _get_new_lines(token.value)
        input_string = input_string.removeprefix(token.value)
        if token.token_type == "UNDEFINED":
            yield token
            return 
        if token.token_type in hidden:
            continue
        yield token
