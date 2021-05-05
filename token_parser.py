from typing import NamedTuple, Tuple, Union
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


def _get_chartoken(pattern: str) -> Tuple[TokenType, int]:
    # \
    if pattern[0] == ESC:
        if pattern[1] not in ESCAPABLE:
            err('pattern has invalid escaped character,', pattern[1])

        return CharToken(pattern[1]), 2

    # (
    if pattern[0] == '(':
        pattern2, inc = _get_paran_pattern(pattern[1:])
        t = regex_to_tokens(pattern2)

        # maybe * after it
        if len(pattern) > inc+1 and pattern[inc+1] == '*':
            return ZeroOrMoreToken(t), inc+2

        return t, inc+1

    # peek *
    if len(pattern) >= 2 and pattern[1] == '*':
        return ZeroOrMoreToken(CharToken(pattern[0])), 2

    # character
    return CharToken(pattern[0]), 1


def _get_paran_pattern(pattern: str) -> Tuple[str, int]:
    count = 1
    for i, c in enumerate(pattern):
        if c == '(':
            count += 1
        if c == ')':
            count -= 1
        if count == 0:
            return pattern[:i], i+1

    err('unreachable')


def regex_to_tokens(pattern: str) -> TokenType:
    """
    regex_to_tokens takes regex pattern and returns token tree
    handles errors in the pattern
    """
    if len(pattern) == 0:
        return CharToken('')

    # META at first
    if pattern[0] in ALL_META:
        err('invalid pattern')
    # non-escaped META at end
    if len(pattern) >= 2 and pattern[-1] in OR_META and pattern[-2] != ESC:
        err('invalid pattern')
    # ESC at end
    if pattern[-1] == ESC:
        err('invalid pattern')
    # paranthesis count
    if pattern.count('(') != pattern.count(')'):
        err('invalid paranthesis, count of "(" is not equal to ")"')

    t, i = _get_chartoken(pattern)

    while i < len(pattern):
        if pattern[i] not in ALL_META:  # and
            c, inc = _get_chartoken(pattern[i:])
            t = AndToken(t, c)
            i += inc
        elif pattern[i] in OR_META:  # or
            # safe to move to next character
            # we know there is no + or | at the end
            i += 1

            c, inc = _get_chartoken(pattern[i:])
            t = OrToken(t, c)
            i += inc
        else:
            err('unreachable')

    return t
