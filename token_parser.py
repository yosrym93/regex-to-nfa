from typing import NamedTuple, Union
from constants import *
from utils import *


class Token:
    pass


class CharToken(NamedTuple):
    # one character
    value: str


class AndToken(NamedTuple):
    a: Token
    b: Token


class OrToken(NamedTuple):
    a: Token
    b: Token


class ZeroOrMoreToken(NamedTuple):
    # token repeated 0 or more times
    a: Token


TokenType = Union[Token, CharToken, AndToken, OrToken, ZeroOrMoreToken]


def _invalid_strs():
    for a in ALL_META:
        for b in ALL_META:
            yield f'{a}{b}'


def _get_chartoken(pattern: str) -> TokenType:
    assert len(pattern) >= 1

    ct = CharToken(pattern[0])

    # peek to see *
    if len(pattern) >= 2 and pattern[1] == '*':
        return ZeroOrMoreToken(ct)
    return ct


def regex_to_tokens(pattern: str) -> TokenType:
    """
    regex_to_tokens takes regex pattern and returns token tree
    handles errors in the pattern
    """
    if len(pattern) == 0:
        return CharToken('')

    # handle all possible errors
    if pattern[0] in ALL_META:
        err('invalid token at index 0')
    if pattern[-1] in OR_META:
        err(f'invalid token at index {len(pattern)}')
    for s in _invalid_strs():
        i = pattern.find(s)
        if i != -1:
            err(f'invalid token at index {i}')

    t = CharToken(pattern[0])
    i = 1
    while i < len(pattern):
        if pattern[i] not in ALL_META:
            t = AndToken(t, _get_chartoken(pattern[i:]))
        elif pattern[i] in OR_META:
            # safe to check next character
            # we know there is no + or | at the end
            i += 1
            t = OrToken(t, _get_chartoken(pattern[i:]))
        else:  # * is handled
            pass

        i += 1

    return t
